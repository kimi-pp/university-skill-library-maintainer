---
name: fintech-research
version: "2.0"
description: Fintech 月报纯搜索阶段 — Phase 1-3（一级信源抓取 → 二级信源搜索 → 聚合去重），支持并行搜索 + 两阶段抓取 + 跨信号放大
argument-hint: "YYYY年MM月"
user-invocable: true
model: opus
effort: high
context: fork
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

# Fintech 月报搜索 Skill

> **职责**：执行全部搜索任务，保存结构化事件数据到 JSON。不做任何分析或报告生成。
>
> **输入**：`/fintech-research 2026年4月`
> **输出**：`~/.claude/fintech-reports/logs/phase3-unique-events.json`

---

## Phase 0: 初始化

### 步骤 1: 解析参数

从参数中提取目标年月：
- 输入格式：`2026年4月` 或 `2026-04`
- 如果无年月参数，默认上个月
- 提取变量：`YYYY`（年份数字）、`MM`（月份数字，如 04）、`month_cn`（中文月名，如 4月）

### 步骤 2: 创建输出目录

```bash
mkdir -p ~/.claude/fintech-reports/{output,logs,data}
```

### 步骤 3: 读取关键知识文件

```python
# 核心玩家图谱（用于优先级排序和完整性检查）
read("../../knowledge-base/core-players.md")
# 搜索任务清单（128 个查询）
read("../../reference/01-search-queries.md")
# 信源分类规则（用于一级信源识别）
read("../../reference/02-source-classification.md")
# 关键词展开映射（用于空结果回退）
read("../../reference/08-keyword-expansion.md")
# 防坑指南
read("../../reference/07-troubleshooting.md")
```

### 步骤 4: 复制宏观指标模板

```bash
cp -r ../../knowledge-base/macro-indicators/templates/* ~/.claude/fintech-reports/data/
```

---

## Phase 1: 一级信源直接抓取（串行执行）

> **原则**：监管新闻必须从官网直接抓取，不接受二手报道

### 1.1 HKMA（香港金管局）

```
WebFetch("https://www.hkma.gov.hk/chi/news-and-media/press-releases/")
→ 提取页面中所有新闻链接
→ 筛选日期在目标月份的新闻
→ 对每条新闻 WebFetch 正文 → 提取标题、日期、正文 → 保存
```

### 1.2 美联储（Fed）

```
WebFetch("https://www.federalreserve.gov/newsevents/pressreleases.htm")
→ 筛选目标月份的新闻 → 提取 Fintech 相关内容
```

### 1.3 欧洲央行（ECB）

```
WebFetch("https://www.ecb.europa.eu/press/pr/date/{YYYY}/html/index.en.html")
→ 筛选目标月份
```

### 1.4 Stripe 官方博客

```
WebFetch("https://stripe.com/newsroom")
→ 筛选目标月份的新闻
```

### 失败处理（P1-1 四级重试链）

**强制按序重试，不得跳过**：
1. **WebFetch** — 直接访问官网 URL，重试 2 次
2. **OpenCLI**（如可用）— 使用浏览器引擎渲染后抓取，适用于 JS 动态加载页面
3. **Playwright**（如可用）— 模拟浏览器行为抓取，适用于反爬网站
4. **搜索转载** — 搜索该页面的内容转载版本，使用 `"site:xxx.com {主题} {YYYY} {MM}"` 定位

**降级规则**：
- 四级重试全部失败 → 记录错误 `{"source": "HKMA", "error": "所有抓取方式均失败", "status": "failed", "attempts": ["WebFetch", "OpenCLI", "Playwright", "search_backup"]}`
- 搜索转载找到内容 → 降级使用搜索摘要，标注 `"source_level": "downgraded"`，并在输出中注明原始来源 URL
- 搜索转载也无结果 → 记录 `{"source": "HKMA", "error": "无法获取内容", "status": "failed"}`

- 如果目标月份无新闻 → 正常结束，记录 `"status": "no_news_for_month"`，不编造
- 所有时间戳必须保留完整日期：`YYYY-MM-DD`，**禁止**只保留 HH:MM

**输出**：`~/.claude/fintech-reports/logs/phase1-primary-sources.json`

---

## Phase 2: 二级信源搜索 + 验证（两阶段策略）

> ⚠️ **核心优化**：两阶段抓取 —— 先扫标题，再抓全文，节省 30-50% token
>
> **并行策略**：将 13 个 Batch 分为 4 组，使用 4 个子 skill 并行搜索（通过 fintech-monthly-report 编排器协调）：
> - Group A: Batch 1-2（支付清结算，29 个查询）
> - Group B: Batch 3-7（金融全品类，41 个查询）
> - Group C: Batch 8-12（主题+监管，33 个查询）
> - Group D: Batch 13（产品级功能发布，25 个查询）
>
> 比赛环境中通过连续 WebSearch 调用执行（模型会自动并行优化）。

### 2.1 两阶段抓取策略

**阶段 A — 快速扫描**（每个查询）：
1. 执行 WebSearch，只获取标题 + URL + 摘要
2. 初步判断信号强度：
   - **高信号**：命中核心玩家 + 关键字（acquisition / regulation / licensing / launch / framework / partnership）
   - **中信号**：命中核心玩家或关键字之一
   - **低信号**：仅有模糊匹配
3. 标记为 `scan_only`，不立即 WebFetch

**阶段 B — 深度抓取**（仅高信号 + 中信号事件）：
1. 对所有高信号事件 + 中信号事件执行 WebFetch
2. 提取标题、日期、正文、作者
3. 验证日期在目标月份
4. 低信号事件保留标题+URL+摘要，不做全文抓取（节省 token）

**节省原理**：128 个查询可能返回 500+ 条搜索结果，只对 ~100 条高/中信号事件做全文抓取，避免对 400+ 条低信号事件浪费 WebFetch。

### 2.2 跨信号放大

当同一事件出现在多个独立信源时，自动提升信号强度：

```python
# URL 去重后，检查同一 URL 是否被多个 Batch 发现
url_sources = {}
for event in all_events:
    if event.url not in url_sources:
        url_sources[event.url] = set()
    url_sources[event.url].add(event["query_source_batch"])

for url, batches in url_sources.items():
    if len(batches) >= 2:
        # 跨信号放大：至少 2 个独立 Batch 都发现该事件
        mark_as_amplified(url)
        # 在评分中增加 bonus（在 Phase 4 中处理）
```

### 2.3 分组搜索策略

**将 13 个 Batch 分为 4 组执行**：

| 组 | 负责的 Batch | 查询数 | 关键词特点 |
|---|-------------|--------|-----------|
| A | Batch 1-2（支付清结算） | 29 | 公司名搜索，英文+中文混合 |
| B | Batch 3-7（金融全品类） | 41 | 消费信贷、数字银行、财富、区块链、AI+金融 |
| C | Batch 8-12（主题+监管） | 33 | 主题搜索、融资并购、咨询报告、监管执法 |
| D | Batch 13（产品级功能发布） | 25 | 竞品产品动态，对标字节业务线 |

**执行方式**：按组顺序执行，每组内查询连续调用 WebSearch。

#### 阶段 A — 快速扫描（每组）

```
for query in assigned_queries:
    # 1. 替换占位符
    search_query = replace_placeholders(query, YYYY, MM)

    # 2. 执行搜索
    results = WebSearch(search_query)

    if not results:
        # 回退 1: 关键词展开（参考 reference/08-keyword-expansion.md）
        expanded = expand_keywords(search_query)
        for variant in expanded[:3]:
            results = WebSearch(variant)
            if results: break

    if not results:
        # 回退 2: 去掉时间限定
        base_variant = remove_time_constraint(search_query)
        results = WebSearch(base_variant)

    if not results:
        record_result(query, [], "no_results")
        continue

    # 对每个结果做初步信号判断
    for r in results[:10]:
        signal_level = assess_signal(r.title, r.snippet, r.url)
        record_scan_result(query, {
            "title": r.title, "url": r.url, "snippet": r.snippet,
            "signal": signal_level  # high / medium / low
        })
```

#### 阶段 B — 深度抓取（仅高/中信号）

```
for item in scanned_items:
    if item.signal in ["high", "medium"]:
        # 执行全文抓取
        content = WebFetch(item.url)
        title = extract_title(content) or item.title
        date = extract_date(content) or extract_date_from_url(item.url)
        summary = extract_summary(content)

        if date_matches_target(date):
            record_verified_event({
                "title": title.strip(),
                "date": normalize_date(date),
                "url": item.url,
                "summary": summary.strip(),
                "verified": True,
                "source": infer_source(item.url)
            })
    else:
        # 低信号：保留标题+URL+摘要，不抓取全文
        record_low_signal_event(item)
```

### 2.4 分组执行

**按组顺序执行，每组完成后保存中间结果**：

**Group A — 支付清结算（Batch 1-2, 29 个查询）**：
- 读取 `../../reference/01-search-queries.md` 中 Batch 1 和 Batch 2 的所有查询
- 执行阶段 A（快速扫描）→ 阶段 B（深度抓取）
- 注意：国际公司用英文关键词，中国公司用中文关键词
- 结果保存到：`~/.claude/fintech-reports/logs/phase2-batch-1-2.json`

**Group B — 金融全品类（Batch 3-7, 41 个查询）**：
- 读取 Batch 3、4、5、6、7 的所有查询
- 注意：区块链与稳定币（Batch 6）是高频造假区域，对 crypto 类事件做更严格的 URL 验证
- AI+金融（Batch 7）注意区分真实产品发布和概念炒作
- 结果保存到：`~/.claude/fintech-reports/logs/phase2-batch-3-7.json`

**Group C — 主题+监管（Batch 8-12, 33 个查询）**：
- 读取 Batch 8、9、10、11、12 的所有查询
- 注意：咨询报告（Batch 11）搜索年份而非月份，用 "{YYYY}" 而非 "{YYYY} {MM}"
- 监管执法（Batch 12）对罚款/牌照吊销事件做更严格验证
- 结果保存到：`~/.claude/fintech-reports/logs/phase2-batch-8-12.json`

**Group D — 产品级功能发布（Batch 13, 25 个查询）**：
- 读取 Batch 13 的所有查询
- 注意：直接对标字节财经业务线，特别关注产品功能细节
- 对 "新功能"/"新特性" 类事件，确认是正式发布而非内测/预告
- 结果保存到：`~/.claude/fintech-reports/logs/phase2-batch-13.json`

**时间戳规则**：
- 所有日期必须保留完整格式 YYYY-MM-DD
- 禁止只保留 HH:MM 时间部分
- 无法确定日期的事件直接剔除

**防幻觉规则**：
- 搜索结果为空时记录空数组，绝不编造事件、URL 或摘要
- 描述事件关联时使用 SVO 句型，区分"相关性"和"因果性"
- 如果某个查询连续无结果，不要反复重试同一关键词

### 2.5 聚合结果

4 个组完成后，读取所有结果：

```
batch_1_2 = read("phase2-batch-1-2.json")
batch_3_7 = read("phase2-batch-3-7.json")
batch_8_12 = read("phase2-batch-8-12.json")
batch_13 = read("phase2-batch-13.json")
```

合并为完整文件：

```
all_results = batch_1_2["results"] + batch_3_7["results"] + batch_8_12["results"] + batch_13["results"]
all_events = batch_1_2["all_events"] + batch_3_7["all_events"] + batch_8_12["all_events"] + batch_13["all_events"]

# 跨信号放大检测
url_to_batches = {}
for event in all_events:
    url = event["url"]
    if url not in url_to_batches:
        url_to_batches[url] = set()
    url_to_batches[url].add(event.get("source_batch", ""))

for event in all_events:
    if len(url_to_batches.get(event["url"], set())) >= 2:
        event["cross_signal_amplified"] = True

output = {
    "target_month": "{YYYY}-{MM}",
    "total_queries_executed": len(all_results),
    "results": all_results,
    "all_events": all_events,
    "cross_signal_amplified_count": count_amplified(all_events)
}
write(output, "phase2-secondary-sources.json")
```

### 2.6 验证完整性

- 如果 `total_queries_executed` < 128 → 提示"部分查询未完成，请手动检查缺失的 Batch"
- 每个查询必须有 entry，即使 events 为空数组（记录 `"status": "no_results"`）
- 哨兵标记检查：确认 4 个 Batch 文件都有 sentinel 标记

---

## Phase 2.5: 头部公司追踪（P2 新增）

> **目标**：对 ~15 家高优先级公司进行月度业务表现和战略动态追踪。
>
> **原则**：公司维度补充事件驱动分析的盲区，覆盖持续性变化（财报、战略调整、人事变动）。

### 步骤 1: 读取追踪名单和公司图谱

```python
# 公司追踪格式规则
read("../../reference/10-company-tracking.md")
# 核心玩家图谱
read("../../knowledge-base/core-players.md")
# 读取上月 company-tracker.json（如存在）
tracker_path = "~/.claude/fintech-reports/data/company-tracker.json"
if tracker_path.exists():
    previous_tracker = read(tracker_path)
```

### 步骤 2: 读取上期追踪数据续接

```python
# 提取上月财务指标和趋势状态
for company in previous_tracker.get("companies", []):
    company.last_metrics = company.financial_metrics
    company.last_strategic_focus = company.strategic_focus
```

### 步骤 3: 逐公司搜索（每家 4-6 个查询）

**对每家高优先级公司执行以下查询**：

| 查询模板 | 示例 |
|---------|------|
| `{公司名} {YYYY} {MM} earnings` | `Stripe 2026 April earnings` |
| `{公司名} {YYYY} {MM} announcement` | `Visa 2026 April announcement` |
| `{公司名} {YYYY} {MM} product launch` | `PayPal 2026 April product launch` |
| `{公司名} {YYYY} quarterly results` | `Nubank 2026 Q1 quarterly results` |
| `{公司中文名} 最新动态 {YYYY}` | `蚂蚁集团 最新动态 2026` |
| `{公司名} acquisition/partnership {YYYY}` | `Block acquisition 2026` |

**一级信源优先**：
- 财报 → 公司 IR 网站或 SEC EDGAR
- 产品发布 → 公司官方博客/Newsroom
- CEO 发言 → 官方新闻稿

**中文公司特殊处理**：
- 蚂蚁集团、腾讯金融科技等使用中文关键词
- 优先从官网/官方渠道获取

### 步骤 4: 提取结构化数据

对每家公司提取：
- **财务指标**：最新季度的收入/交易规模/用户数/净利润等
- **重大事件**：本月产品发布、收购、战略合作、人事变动等
- **战略焦点**：本月体现的战略方向
- **趋势方向**：关键指标 vs 上月的变化方向（上升/持平/下降）

### 步骤 5: 保存到中间文件

```json
{
  "target_month": "2026-04",
  "companies_tracked": 15,
  "companies_with_events": 8,
  "companies": [
    {
      "name": "Stripe",
      "track": "支付清结算",
      "priority": "highest",
      "financial_metrics": {
        "last_reported_quarter": "2025-Q4",
        "key_metric_name": "收单交易规模",
        "key_metric_value": "1.4万亿美金",
        "key_metric_yoy": "+38%",
        "trend_direction": "上升"
      },
      "monthly_events": [
        {
          "date": "2026-04-10",
          "title": "发布 Agentic Payment 框架",
          "url": "...",
          "summary": "...",
          "event_type": "product_launch"
        }
      ],
      "strategic_focus": ["AI + 支付", "稳定币"],
      "bytedance_relevance": {
        "relevance_level": "高",
        "affected_products": ["抖音支付", "TikTok Shop 支付"]
      }
    }
  ]
}
```

**输出**：`~/.claude/fintech-reports/logs/phase2.5-company-research.json`

---

## Phase 3: 聚合与去重

### 步骤 1: 读取所有结果

```python
primary = read("phase1-primary-sources.json")
secondary = read("phase2-secondary-sources.json")
```

### 步骤 2: 去重

```python
seen_urls = set()
unique_events = []

for event in primary["events"] + secondary["all_events"]:
    if event.url in seen_urls:
        continue
    seen_urls.add(event.url)
    unique_events.append(event)
```

### 步骤 3: 完整性检查

必须检查以下类型的事件是否已被覆盖，如有缺失则补充搜索：
- 支付公司并购 / 收购事件
- 核心玩家新产品 / 新框架 / 新协议发布
- 稳定币监管 / 牌照发放
- AI + 支付 / 金融科技新进展
- 数字银行牌照 / 合规进展
- 监管执法 / 罚款 / 牌照吊销
- 跨境支付互联新政策 / 新合作
- 核心公司季度财报 / 重大业务数据
- TikTok Shop 支付 / 电商金融相关动态
- 拉美/东南亚区域重大支付创新
- 竞品产品级功能发布

### 步骤 4: 保存结果

```json
{
  "target_month": "{YYYY}-{MM}",
  "total_events": <count>,
  "events": [...],  // 去重后的完整事件列表
  "primary_count": <count>,
  "secondary_count": <count>,
  "cross_signal_amplified_count": <count>,
  "low_signal_unverified_count": <count>
}
```

**输出**：`~/.claude/fintech-reports/logs/phase3-unique-events.json`

---

## 完成后提示

```
✅ Research 阶段完成！

搜索统计：
- 一级信源：X 条
- 二级信源：X 条
- 去重后总事件：X 条
- 跨信号放大事件：X 条（多信源重合，可信度更高）
- 低信号未验证事件：X 条（保留标题+摘要，未抓全文）

数据已保存到：
- ~/.claude/fintech-reports/logs/phase3-unique-events.json

下一步请执行分析：
/fintech-analysis {YYYY}年{MM}月
```
