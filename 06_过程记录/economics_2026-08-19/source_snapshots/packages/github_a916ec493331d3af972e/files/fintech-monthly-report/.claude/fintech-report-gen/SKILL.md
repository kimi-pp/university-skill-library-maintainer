---
name: fintech-report-gen
version: "2.0"
description: Fintech 月报报告生成阶段 — Phase 6-8（Markdown → HTML → 质量校验 + 动态折叠策略）
argument-hint: "YYYY年MM月"
user-invocable: true
model: opus
effort: high
context: fork
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

# Fintech 月报报告生成 Skill

> **职责**：读取分析数据，生成 Markdown 和 HTML 报告，运行质量校验。
>
> **前置条件**：必须先执行 `/fintech-research` 和 `/fintech-analysis` 完成搜索和分析。
>
> **输入**：`/fintech-report-gen 2026年4月` 或 `/fintech-report-gen 2026年4月 --template consulting-grade`
> **输入数据**：`phase3-unique-events.json` + `phase4-scored-events.json` + `phase5-analysis.md`
> **输出**：`fintech-report-{YYYYMM}-vN.md` + `fintech-report-{YYYYMM}-vN.html`

> **注意**：比赛环境中仅有 WebSearch/WebFetch/Read/Write 工具，不使用 Bash 脚本验证。

---

## Phase 0: 初始化

### 步骤 1: 解析参数

提取 `YYYY`、`MM`、`YYYYMM`

### 步骤 2: 验证数据文件存在

```bash
ls ~/.claude/fintech-reports/logs/phase4-scored-events.json
ls ~/.claude/fintech-reports/logs/phase5-analysis.md
```
- 任一不存在 → 报错"请先完成搜索（/fintech-research）和分析（/fintech-analysis）阶段"

### 步骤 3: 读取分析数据

```python
scored_events = read("~/.claude/fintech-reports/logs/phase4-scored-events.json")
phase5_analysis = read("~/.claude/fintech-reports/logs/phase5-analysis.md")
phase3_data = read("~/.claude/fintech-reports/logs/phase3-unique-events.json")
```

### 步骤 4: 读取格式规范

```python
read("../../reference/04-phase6-markdown-format.md")
read("../../reference/05-html-output-format.md")
```

### 步骤 5: 确定报告模板

使用标准月报格式模板（v2）：

```python
template = read("../../examples/markdown-template-v2.md")
```

> 注：`consulting-grade` 模板选项暂不可用，使用默认模板即可满足咨询级分析要求（分析框架、论证结构等由 Phase 5 分析结果提供）。

### 步骤 6: 确定报告版本号（P2 新增）

版本号格式：`fintech-report-{YYYYMM}-vN`，N 从 1 开始递增。
- 如果 `output/` 目录下已有同名月份报告，版本号 +1
- 版本号写入报告头部：`**报告编号：** FMR-{YYYYMM}-v{N}`

### 步骤 7: 确定报告折叠策略

```python
total_events = len(scored_events.get("events", []))

if total_events < 20:
    # 事件较少：展示全部
    collapse_strategy = "none"
elif total_events < 50:
    # 事件适中：按类别折叠次要事件
    collapse_strategy = "by_category"
else:
    # 事件过多：只展示 ≥60 分事件，其余归档到附录
    collapse_strategy = "score_threshold"
    # 确定阈值
    score_threshold = 60
```

**折叠策略说明**：
- `none`：所有事件完整展示（适用于事件 < 20 条）
- `by_category`：按主题分类展示，每个类别下折叠 60 分以下事件为链接（适用于 20-50 条）
- `score_threshold`：正文只展示 ≥60 分事件，<60 分事件在附录中以链接列表形式呈现（适用于 >50 条）

---

## Phase 6: Markdown 报告生成

> ⚠️ 写入 Markdown 后**必须立即进入 Phase 7 生成 HTML**，不得停留。

**严格按照 `../../reference/04-phase6-markdown-format.md` 中的格式要求生成**：

### 必须包含的章节（按顺序）

1. **报告标题和统计信息**
   ```
   # 全球金融科技月度报告 {YYYY}年{MM}月（{start_date} - {end_date}）
   ```
   包含：总事件数、深度分析数、关注事件数、各信源等级数量

2. **核心结论（Executive Summary）**
   - 3-5 条核心判断，每条包含对字节的战略含义
   - 结论先行，每条一句话

3. **全球宏观指标监测**
   - Mermaid 图表：央行基准利率趋势
   - 全球稳定币市值柱状图
   - 分区域核心指标表格（中国含香港地区/美国/东南亚），香港作为中国下一级子区域嵌套展示
   - 宏观趋势解读（1-3 句话）

4. **本月行业动态（按主题分类）**

   **使用通用事件卡片模板 + 主题差异规则**（P2 改进）：

   ```markdown
   # 通用事件卡片模板：
   - **[{score}] [{事件标题}]({url})** — {一句话摘要}
     {如果≥80分，展开完整六维度深度分析}
   ```

   按以下主题组织：
   - **监管政策动态**（按区域：中国（含香港地区作为子区域）/欧美/东南亚）
   - **投融资与并购动态**（按交易规模从大到小）
   - **头部玩家战略动态**（支付/消费金融/数字银行/其他）
   - **新产品 / 新功能发布**（含对标字节业务分析）
   - **国内竞品动态**（支付宝碰一下/微信分付等）
   - **稳定币、区块链与加密支付动态**

   各主题差异规则（参考 Phase 6 格式文件）：
   - 监管：按区域分组，一级信源事件置顶
   - 并购：标注交易金额 + 标的
   - 新产品：标注对标字节业务线 + 可借鉴点
   - 国内竞品：标注用户规模/增速 + 与字节对应业务线的差距
   - 稳定币：区分实质落地和概念阶段

4.5 **头部公司追踪**（P2 新增）

   在"本月行业动态"之后、"趋势判断"之前，插入头部公司追踪章节。

   ```python
   # 读取公司追踪数据
   company_data = read("~/.claude/fintech-reports/logs/phase2.5-company-research.json")
   company_tracker = read("~/.claude/fintech-reports/data/company-tracker.json")
   # 读取公司追踪格式规则
   read("../../reference/10-company-tracking.md")
   ```

   **报告结构**（按以下格式为每家追踪公司生成卡片）：

   ```markdown
   ## 头部公司追踪

   > 本月追踪 {N} 家公司，{M} 家有重大事件更新

   ### {公司名称}（{赛道}）

   **业务表现**：
   - {关键指标}：{数值}（同比 {变化}）→ 【{趋势方向}】
   - {最新财报季度}：{简要总结}

   **本月重大事件**：
   - {事件 1}（{日期}）— {一句话摘要}
   - 如该公司有 ≥80 分事件，引用事件分析链接而非重复完整分析

   **战略要点**：
   - {战略动向 1}
   - {战略动向 2}

   **护城河变化**：→ {加深/持平/侵蚀}
   - {具体维度变化}

   **对字节启示**：
   - {战略启示}
   ```

   **筛选规则**：
   - 有本月重大事件或财报的公司 → 完整展示（业务表现 + 重大事件 + 战略要点 + 护城河 + 字节启示）
   - 连续 2 个月无重大事件的公司 → 缩减为 1 行简表：`**{公司}**（{赛道}）：{关键指标}，{趋势方向}`
   - 财报季优先展示最新财务数据

   **报告长度控制**：
   - 有事件公司 ≤ 5 家：所有公司完整展示
   - 有事件公司 5-10 家：有重大事件的完整展示，其余缩为简表
   - 有事件公司 > 10 家：只展示 Top 5 有重大事件的公司，其余归档到附录

   **与事件驱动分析的协同**：
   - 公司追踪卡片中不重复事件驱动分析的完整六维度
   - 如果某公司本月有 ≥80 分事件，在卡片中简要引用并链接到事件分析
   - 如果某公司无重大事件但有财报发布，以财报数据为主展示

5. **趋势判断**（3-5 条）
   - 每条：方向 + 阶段 + 论据 + 竞争格局重塑 + 对字节启示 + 可验证预测 + 证伪条件
   - 标注跨月趋势状态：`[续接/新识别/证伪/加强]`

6. **非共识观察**（3-5 条）
   - 每条：市场共识 → 我的判断 → 支撑论据 → 证伪条件 → 对字节启示

7. **字节财经月度竞争态势总结（强制）**
   - 本月关键信号（3-5 条）
   - 按业务线的威胁与机会矩阵
   - 护城河月度变化追踪
   - 竞争窗口期追踪

8. **相关深度报告 & 咨询报告**

9. **信源质量统计**
   - 总体概览 + 信源分级分布 + 信源明细

10. **完整事件清单**（按 5 个类别分组 + 折叠策略）

    **所有策略下都必须按以下 5 个类别分组**：监管政策动态 / 投融资与并购动态 / 新产品与功能发布 / 国内竞品动态 / 稳定币与区块链

    ```markdown
    # 策略 none：全部展示，按类别分组
    ### 监管政策动态
    | 序号 | 日期 | 子区域 | 标题 | 评分 | 信源等级 | 来源 |
    ### 投融资与并购动态
    | 序号 | 日期 | 标题 | 评分 | 信源等级 | 来源 |
    ...（每个类别独立表格）

    # 策略 by_category：按类别折叠
    ### 监管政策动态
    - [完整展示 60+ 分事件]
    <details><summary>其他 X 条低评分事件</summary>
    - [60分以下事件以链接列表呈现]
    </details>

    # 策略 score_threshold：只展示 ≥60 分
    ### 监管政策动态
    | 序号 | 日期 | 子区域 | 标题 | 评分 | 来源 |
    ## 附录：其他事件（<60分）
    [以链接列表呈现，包含标题和 URL]
    ```

### 语言规则
- 面向用户内容必须使用中文
- 品牌名/产品名保留英文
- 外文引言保留原文 + 中文翻译
- 专业术语首次出现必须括号解释

### 叙事质量标准（引用 `../../reference/09-analysis-methodology.md`）
- **标题写结论，不写标签**：章节标题和小标题必须是判断性陈述句，不是名词标签
  - ❌ `监管动态` → ✅ `香港虚拟资产牌照框架正式生效，首批5家机构获批`
- **金字塔原理（结论先行）**：每段第一句必须是结论，后续为支撑论据
- **数据 → 心理 → 战略链**：每个洞察必须连接数据 → 行为变化 → 战略含义，不能只说"X增长，建议关注"
- **证据分级**：≥80 分事件的核心主张必须至少 B 级证据

### 反幻觉检查
生成后必须确认：
- 无 `[待填写]` 占位符
- 无 `TODO` 占位符
- 无 `{{...}}` 占位符
- 所有事件 URL 可点击且非 404
- 事件描述使用 SVO 句型，无虚假因果推断

**输出**：`~/.claude/fintech-reports/output/fintech-report-{YYYYMM}-v{N}.md`

---

## Phase 7: HTML 报告生成

> ⚠️ 本 Phase 必须执行，不得跳过。必须逐条替换占位符，不能直接输出模板。

### 步骤 1: 读取完整模板

```python
template = read("../../examples/html-template.html")
```

### 步骤 2: 创建替换映射表

按 `../../reference/05-html-output-format.md` 中的映射表逐一替换：

| 占位符类别 | 说明 |
|-----------|------|
| 基础信息 | `{{YYYY}}年{{MM}}月`（标题+导航） |
| 宏观指标 | 中国（含香港地区作为子区域）/美国宏观指标行 + 趋势解读 |
| 核心结论 | 关键发现标题 + 描述 + 评分 + 趋势卡片 |
| 非共识观察 | 观察标题 + 描述 |
| 信源统计 | 事件总数/高评分数/各信源等级数量占比/明细分列表 |
| 事件卡片 | 按类别分组展示（监管政策/投融资与并购/新产品新功能/国内竞品/稳定币区块链），每组内按评分排序 |
| 深度分析卡片 | 前三名事件的描述/信号/背景/影响/缺口/行动 + 引用原文 |
| 趋势判断 | 趋势标题/描述/要点1-4 |
| 字节竞争态势 | 关键信号/威胁机会矩阵/窗口期 |
| 头部公司追踪（P2 新增） | 公司名称/业务表现/重大事件/战略要点/护城河变化/字节启示 |

### 步骤 3: 逐一替换

**事件列表卡片**：
- 从 `phase4-scored-events.json` 中按评分排序
- 逐条替换 `{{事件标题}}` / `{{事件URL}}` / `{{事件描述}}` / `{{评分}}` / `{{类别}}` / `{{来源名称}}` / `{{日期}}`

**深度分析卡片（前三名事件）**：
- 从 `phase4-scored-events.json` 中获取前三名事件的描述、信号、背景、影响、缺口、行动
- 从原文中提取引用原文
- 替换 `{{事件N标题}}` / `{{事件N描述}}` / `{{事件N信号}}` / `{{事件N背景}}` / `{{事件N影响}}` / `{{事件N缺口}}` / `{{事件N行动}}` / `{{事件N引用原文}}` / `{{事件N来源名称}}`（N=1,2,3）
- 布局：事件描述放顶部（`event-desc-section`），深度分析分两栏（左：信号+背景，右：影响+缺口+行动），底部放引用原文（`quote-block`）

**趋势判断 Tab**：
- 从 `phase5-analysis.md` 中提取趋势判断
- 替换 `{{趋势N标题}}` / `{{趋势N描述}}` / `{{趋势N要点1}}` ~ `{{趋势N要点4}}`

**概述 Tab - 相关报告**：
- 从 Phase 2 Batch 11 结果中提取咨询报告
- 替换 `{{行业报告列表}}`

**地区统计（regionData）**：
- 按事件地区统计，必须包含 events 数组

**引言格式**（score ≥ 80 的事件）：
- 外文：英文原文 + 中文翻译 + 来源
- 中文：直接引用 + 来源

### 步骤 4: 验证所有占位符已替换

读取 HTML 文件，搜索 `{{` 字符串。
- 如果仍有 `{{` 占位符 → 必须立即替换，不能跳过

### 步骤 4.5: 验证 JS 语法完整性

读取 HTML 文件的 `<script>` 部分，检查：
- **`</script>` 前不能有独立的 `});`** — 这会导致整个 script 块解析失败
- `switchTab`、`jumpToTab`、`initWorldMap`、`initMacroChart` 函数定义完整
- `var macroChartInstance = null;` 全局变量存在

### 步骤 5: 保存输出

**输出**：`~/.claude/fintech-reports/output/fintech-report-{YYYYMM}-v{N}.html`

---

## Phase 8: 质量校验

> **比赛环境适配**：不使用 Bash/Python 脚本，通过 Read 工具手动检查。

### 手动质量检查清单

**步骤 1: 检查 Markdown 报告**
```
read("~/.claude/fintech-reports/output/{report_md}")
```
检查项：
- [ ] 无 `[待填写]` 占位符
- [ ] 无 `TODO` 占位符
- [ ] 无 `{{...}}` 占位符
- [ ] 所有事件 URL 可点击且非 404
- [ ] 事件描述使用 SVO 句型，无虚假因果推断
- [ ] 事件标题包含中文
- [ ] 各信源等级数量统计正确

**步骤 2: 检查 HTML 报告**
```
read("~/.claude/fintech-reports/output/{report_html}")
```
检查项：
- [ ] 无 `{{` 剩余占位符
- [ ] `</script>` 前没有独立的 `});`
- [ ] `switchTab`、`jumpToTab`、`initWorldMap`、`initMacroChart` 函数定义完整
- [ ] `var macroChartInstance = null;` 全局变量存在

**步骤 3: 检查数据文件完整性**
```
read("~/.claude/fintech-reports/logs/phase3-unique-events.json")
read("~/.claude/fintech-reports/logs/phase4-scored-events.json")
read("~/.claude/fintech-reports/logs/phase5-analysis.md")
```
检查项：
- [ ] 各阶段日志文件存在且非空
- [ ] trend-tracker.json 已更新

**步骤 4: URL 抽检**
对报告中 ≥80 分事件的 URL 使用 WebFetch 进行可访问性抽检（至少 3 条）。

### 结果处理

- **成功（exit 0）** → 报告完整，继续 Phase 9
- **失败（exit 1）** → 根据错误提示修复，重新生成缺失部分，再次运行校验

---

## Phase 9: 飞书发布（可选）

> **触发条件**：存在 `FEISHU_APP_ID` 环境变量 或 `~/.local/bin/lark-cli` 可用

### 步骤 1: 检测飞书发布能力

```bash
# 方式 1: 环境变量
echo $FEISHU_APP_ID
# 方式 2: lark-cli
~/.local/bin/lark-cli --version
```

### 步骤 2: 发布到飞书

如果具备发布能力：

```bash
python3 ../../scripts/publish-to-feishu.py {YYYYMM}
```

可选参数：
- `--title "自定义标题"` — 覆盖默认文档标题
- `--folder-token TOKEN` — 指定目标文件夹（从飞书 URL 获取）

### 步骤 3: 处理结果

- **成功**：输出飞书文档 URL，提示用户
- **失败**：记录错误原因，不影响报告生成流程，提示用户手动发布

### 失败降级方案

如果自动发布失败：
1. 提示用户 Markdown 报告路径
2. 说明可直接复制到飞书文档（飞书支持 Markdown 粘贴）
3. 不阻塞整体流程

---

## 完成后提示

```
✅ 报告生成完成！

输出文件：
- ~/.claude/fintech-reports/output/fintech-report-{YYYYMM}.md
- ~/.claude/fintech-reports/output/fintech-report-{YYYYMM}.html

质量校验：✅ 所有检查通过
（或：❌ 发现 X 个问题，已自动修复）

飞书发布：✅ 已发布 → https://bytedance.larkoffice.com/docx/xxx
（或：⏭️  未配置飞书凭证，跳过发布）
（或：❌ 发布失败: {错误原因}，请手动复制 Markdown 到飞书）
```
