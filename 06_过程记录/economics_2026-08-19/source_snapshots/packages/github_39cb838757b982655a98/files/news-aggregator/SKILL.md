---
name: news-aggregator
version: "1.0.0"
description: 使用 WebSearch/WebFetch 从多信源聚合新闻，支持中文输出、去重、分类、深度分析
user-invocable: true
model: opus
effort: medium
context: fork
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

# News Aggregator Skill

使用 Claude Code 内置 WebSearch/WebFetch 工具从多信源聚合新闻，进行去重、分类、深度分析，生成中文报告。

无需外部 Python 脚本或 API 密钥。

> **与 `/ai-news` 的分工**：
> - `/ai-news`：专注 **AI/ML 垂直领域**（模型发布、研究突破、AI 编程工具、中国 AI 实验室）
> - `/news-aggregator`：专注 **通用新闻/行业报道**（金融科技、商业、政策、市场、科技综合）
> - 用户请求"AI 新闻"时使用 `/ai-news`，请求"行业新闻"/"综合资讯"时使用 `/news-aggregator`

---

## 支持信源

### 优先级说明

**Tier 1（必抓，最高优先级）**：核心监管源 + 顶级通讯社，信息权威性最高
**Tier 2（重要）**：行业头部公司官方博客 + 权威科技媒体
**Tier 3（补充）**：垂直媒体 + 综合科技媒体，用于发现长尾信号

### 全球综合新闻
| 优先级 | 信源 | 抓取方式 | URL |
|--------|------|----------|-----|
| Tier 1 | Reuters Business | WebSearch | reuters business fintech news |
| Tier 1 | Bloomberg | WebSearch | bloomberg fintech markets news |
| Tier 1 | Financial Times | WebSearch | financial times fintech latest |
| Tier 1 | 华尔街见闻 | WebFetch | https://wallstreetcn.com/ |
| Tier 2 | Hacker News | WebFetch | https://news.ycombinator.com/ |
| Tier 2 | 36氪 | WebFetch | https://36kr.com/ |
| Tier 2 | TechCrunch | WebFetch | https://techcrunch.com/ |

### AI/科技
| 优先级 | 信源 | 抓取方式 | URL |
|--------|------|----------|-----|
| Tier 2 | The Verge | WebFetch | https://www.theverge.com/tech |
| Tier 3 | Ars Technica | WebFetch | https://arstechnica.com/ |
| Tier 3 | Product Hunt | WebFetch | https://www.producthunt.com/ |
| Tier 3 | AI News | WebSearch | AI fintech news today |

### 中文科技/商业
| 优先级 | 信源 | 抓取方式 | URL |
|--------|------|----------|-----|
| Tier 1 | 财新网 | WebSearch | 财新 金融科技 最新 |
| Tier 2 | 虎嗅 | WebFetch | https://www.huxiu.com/ |
| Tier 2 | 界面新闻 | WebFetch | https://www.jiemian.com/ |
| Tier 3 | 晚点LatePost | WebSearch | 晚点LatePost 最新文章 |

### 中国 Fintech 专项（新增）
| 优先级 | 信源 | 抓取方式 | URL |
|--------|------|----------|-----|
| Tier 1 | 中国人民银行 | WebFetch | https://www.pbc.gov.cn/ |
| Tier 2 | 零壹财经 | WebSearch | 零壹财经 金融科技 |
| Tier 3 | 未央网 | WebFetch | https://www.weiyangx.com/ |

### RSS 聚合（可选）
| 信源 | 抓取方式 |
|------|----------|
| RSS 源列表 | WebFetch XML 解析 |

---

## Workflow

### 模式一：快速扫描

```
/news-aggregator --mode scan --sources hackernews,36kr,wallstreetcn --keyword fintech
```

1. **并行抓取**各信源最新内容（WebSearch/WebFetch）
2. **过滤**：按关键词、时间范围（默认 24h）
3. **去重**：标题相似度 >80% 或同 URL 合并
4. **分类**：按类别分组输出摘要

### 模式二：深度报告

```
/news-aggregator --mode report --sources all --keyword "金融科技" --deep
```

1. **并行抓取**全部信源
2. **深度阅读**：对高价值条目使用 WebFetch 阅读全文
3. **分析**：背景、影响、趋势判断
4. **输出**：结构化中文报告

### 模式三：每日简报

```
/news-aggregator --mode daily-briefing
```

预配置的多信源组合，生成每日资讯简报。

---

## 抓取策略

### WebSearch 模式

```
WebSearch(query: "<keyword> news today", allowed_domains: ["domain.com"])
```

适用于无 RSS 或反爬严格的站点。

### WebFetch 模式

```
WebFetch(url: "https://site.com/rss", prompt: "Extract all items from the past 24 hours")
```

适用于 RSS/Atom feed 或 HTML 列表页。

### 并行策略

独立信源并行抓取，同一信源内分批次：
- 批次 1：聚合器/首页
- 批次 2：细分频道
- 批次 3：深度阅读（仅高价值条目）

---

## 去重与分类

### 去重规则

1. 精确标题匹配 → 合并
2. URL 相同 → 保留信息量最大的版本
3. 标题相似度 >80% → 标记为同一事件，保留最优来源

### 分类体系

| 类别 | 关键词 |
|------|--------|
| 融资/投资 | funding, investment, round, acquisition, IPO |
| 产品发布 | launch, release, announce, new feature |
| 政策/监管 | regulation, policy, compliance, fine |
| 人事变动 | hire, CEO, appoint, fire, layoff |
| 市场动态 | market, growth, trend, share |
| 技术突破 | breakthrough, research, paper, benchmark |
| 行业分析 | analysis, report, insight, study |

---

## 报告模板

```markdown
# 资讯报告
**日期**: YYYY-MM-DD
**信源**: N 个信源
**时间范围**: 过去 24 小时
**关键词**: [筛选条件]

---

## 融资/投资
1. **[中文标题](原文链接)**
   - 来源: 信源名 | 时间: HH:MM
   - 摘要: 一句话中文摘要
   - 分析: 💡 背景、影响、战略含义

## 产品发布
...

## 政策/监管
...

## 市场动态
...

## 技术突破
...
```

---

## 规则

1. **语言**：简体中文输出，保留知名英文专有名词
2. **时间**：必须字段，缺失时标注 "Unknown Time"
3. **反幻觉**：仅使用抓取到的数据，不编造新闻
4. **智能关键词扩展**：
   - "AI" → "AI,LLM,GPT,Claude,Agent,RAG,DeepSeek"
   - "金融科技" → "金融科技,fintech,支付,区块链,数字银行,数字人民币"
   - "Web3" → "Web3,crypto,blockchain,DeFi,NFT,token"
5. **信源标记**：每条新闻标注原始来源和时间
6. **保存**：报告保存到 `reports/YYYY-MM-DD/` 目录

## 参数

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `--mode` | scan / report / daily-briefing | report |
| `--sources` | 信源，逗号分隔 | all |
| `--keyword` | 关键词筛选 | 无 |
| `--deep` | 深度阅读高价值条目 | 关闭 |
| `--hours` | 时间范围（小时） | 24 |
| `--save` | 保存到文件 | 自动 |
