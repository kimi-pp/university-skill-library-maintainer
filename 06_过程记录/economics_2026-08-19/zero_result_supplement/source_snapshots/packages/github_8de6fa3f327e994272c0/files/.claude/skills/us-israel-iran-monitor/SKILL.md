---
name: us-israel-iran-monitor
description: Monitor and analyze recent events related to the US-Israel-Iran conflict (美以伊战争/冲突), storing structured impact analyses in the `events/us-israel-iran/` directory of the current project. Use this skill whenever the user asks to track, monitor, analyze, or research news about the US-Israel-Iran war, Middle East geopolitical tensions, Iran nuclear deal, US-Iran sanctions, Israel-Iran military confrontations, or related events that affect oil prices, gold, US stocks, or Chinese ADRs. TRIGGER when the user says things like "监控美以伊", "美以伊战争最新", "中东局势", "伊朗局势", "以色列伊朗冲突", "monitor US-Israel-Iran", "Middle East conflict update", or asks about geopolitical impact on oil/gold/defense stocks.
---

# 美以伊冲突动态监控与分析 Skill

This skill searches for recent events related to the US-Israel-Iran conflict, analyzes each event's geopolitical and market impact, stores results in structured markdown files, and deduplicates to avoid re-analyzing events already on record.

## Workflow Overview

1. **Search** for recent US-Israel-Iran conflict events using web search
2. **Deduplicate** against already-analyzed events
3. **Analyze** each new event's impact
4. **Store** results in `events/us-israel-iran/events/` as markdown files
5. **Update** the index and deduplication registry
6. **Notify** via Feishu

---

## Step 1 — Set up directory structure

Ensure these paths exist in the current working directory:

```
events/us-israel-iran/
├── index.md              ← Running list of all analyzed events
├── analyzed_events.json  ← Deduplication registry
└── events/               ← One .md file per analyzed event
```

Create them if they don't exist. For `analyzed_events.json`, initialize as:
```json
{"events": []}
```

For `index.md`, initialize with a header:
```markdown
# 美以伊冲突事件分析索引

| 日期 | 标题 | 影响评级 | 文件 |
|------|------|----------|------|
```

---

## Step 2 — Search for recent events

Use **multiple search queries** to cast a wide net. Run 4–6 of these:

- `US Israel Iran war latest news 2026`
- `美以伊战争 最新动态 2026`
- `Iran nuclear deal military strike Israel 2026`
- `Iran Israel US military conflict update`
- `Middle East geopolitical tension oil price 2026`
- `伊朗 以色列 美国 军事 外交 最新`
- `Iran sanctions IRGC US strike latest`
- `Israel Iran war escalation ceasefire`
- `美以伊 局势 石油 黄金 影响`

Collect all results. For each result, record:
- **title** (标题)
- **date** (日期, ISO format if available, else approximate)
- **source** (来源)
- **url** (链接)
- **summary** (摘要, 1–2 sentences from the search result)

---

## Step 3 — Deduplicate

Read `events/us-israel-iran/analyzed_events.json`. For each collected event:

- Check if the URL already appears in `analyzed_events.json["events"][*]["url"]`
- Also check for near-duplicate titles: if the title is >80% similar to an existing title (same event, different source), skip it
- Only proceed with **genuinely new** events not yet in the registry

If all events are already analyzed, report this to the user and stop.

---

## Step 4 — Analyze each new event

For each new event, produce a structured impact analysis. Think carefully about:

- **What happened**: A factual summary of the event (2–4 sentences)
- **军事/外交直接影响**: Immediate military or diplomatic effects — strikes, negotiations, sanctions, troop movements, UN resolutions
- **石油价格影响**: How this event affects crude oil (Brent/WTI) — supply disruption risk, Strait of Hormuz threat, OPEC response
- **全球金融市场影响**: Impact on gold (safe-haven demand), US stocks (defense sector, energy), Chinese ADRs (risk appetite, supply chain)
- **中东地缘格局变化**: Shifts in regional alliances — Hezbollah, Hamas, Saudi Arabia, UAE, Turkey, Russia/China positioning
- **投资者视角**: How this may affect crude oil ETFs (USO, OIL), gold (GLD, XAU), defense stocks (LMT, RTX, NOC), and Chinese ADRs
- **Impact rating**: Choose one: 🔴 局势升级 / 🟡 局势平稳 / 🟢 局势缓和 / ⚪ 低影响

Consider the current strategic context when analyzing:
- Iran's nuclear enrichment progress and IAEA inspections
- Israeli military posture and domestic political pressures
- US election cycle and administration policy toward Iran
- Strait of Hormuz as global oil chokepoint (~20% of global oil supply)
- Proxy conflicts: Hezbollah (Lebanon), Houthis (Yemen), Hamas (Gaza)
- Russia/China support for Iran and US response

---

## Step 5 — Write event files

For each analyzed event, create a file at:
```
events/us-israel-iran/events/YYYY-MM-DD_<slug>.md
```

Where `<slug>` is a short kebab-case English title (e.g., `iran-nuclear-strike-threat`, `us-sanctions-expanded`, `ceasefire-talks-geneva`).

Use this exact template:

```markdown
# [Event Title in Chinese or English]

**日期 / Date:** YYYY-MM-DD  
**来源 / Source:** [Source Name](URL)  
**影响评级 / Impact Rating:** 🔴 局势升级 *(or whichever applies)*

---

## 事件摘要 / Summary

[2–4 sentence factual description of what happened]

---

## 军事/外交直接影响 / Military & Diplomatic Impact

[Immediate military operations, diplomatic moves, sanctions, UN/bilateral responses]

---

## 石油价格影响 / Oil Price Impact

[Effect on Brent/WTI crude, Strait of Hormuz risk, OPEC+ positioning, energy supply disruption probability]

---

## 全球金融市场影响 / Global Financial Market Impact

[Gold safe-haven demand, US equity market reaction, defense sector outlook, Chinese ADR risk appetite]

---

## 中东地缘格局变化 / Middle East Geopolitical Shifts

[Regional alliance changes: Hezbollah, Houthis, Saudi/UAE stance, Russia/China positioning]

---

## 投资者视角 / Investor Angle

[How this affects: 原油ETF (USO/OIL), 黄金 (GLD/XAU), 防务股 (LMT/RTX/NOC), 中概股 risk premium]

---

## 风险与机遇 / Risk & Opportunity

**Overall:** [局势升级 / 局势平稳 / 局势缓和 / 低影响]  
[1–3 sentences explaining the net geopolitical and market assessment]
```

---

## Step 6 — Update the registry and index

**Update `events/us-israel-iran/analyzed_events.json`** — append each new event:

```json
{
  "events": [
    {
      "url": "https://...",
      "title": "Event title",
      "date": "YYYY-MM-DD",
      "file": "events/us-israel-iran/events/YYYY-MM-DD_slug.md",
      "impact_rating": "局势升级",
      "analyzed_at": "YYYY-MM-DDTHH:MM:SSZ"
    }
  ]
}
```

**Update `events/us-israel-iran/index.md`** — add a row to the table for each new event:

```markdown
| YYYY-MM-DD | [Event title](events/YYYY-MM-DD_slug.md) | 🔴 局势升级 | [link](events/YYYY-MM-DD_slug.md) |
```

---

## Step 7 — Report to the user

After completing all analyses, provide a concise summary:

```
## 本次监控结果 / Monitoring Results

发现 X 个新事件，已跳过 Y 个重复事件。

### 新分析事件：
1. **[事件标题]** — [Impact Rating] — `events/us-israel-iran/events/...md`
2. ...

所有分析已保存至 `events/us-israel-iran/` 目录。
```

---

## Step 8 — Send Feishu notification (if configured)

After reporting to the user, send a Feishu notification using the **feishu-notify** skill. Run:

```bash
python3 scripts/feishu_notify.py \
  --title "🌍 美以伊冲突动态监控报告" \
  --item "发现 X 个新事件，跳过 Y 个重复" \
  --entry "event:[影响评级emoji] [事件标题1]" \
  --entry "detail:[军事/外交核心事实，1句话]" \
  --entry "detail:石油/黄金影响: [简述原油价格走向或避险需求]" \
  --entry "detail:市场视角: [防务股/中概股/原油ETF影响简述]" \
  --entry "event:[影响评级emoji] [事件标题2]" \
  --entry "detail:[核心事实]" \
  --entry "detail:石油/黄金影响: [简述]" \
  --entry "detail:市场视角: [简述]" \
  --footer "📁 详情: ~/stock-analysis/events/us-israel-iran/"
```

- For each event: always include 3 `--entry detail:` lines — military/diplomatic fact, oil/gold impact, and market angle
- If no new events found: `--item "✅ 今日无新事件（已跳过 Y 个重复）"` (no `--entry` needed)
- If `scripts/feishu_notify.py` doesn't exist or `.env` is not configured, skip silently — don't fail the task
- See the **feishu-notify** skill for setup instructions

---

## Important notes

- **Language**: Write event files in bilingual format (Chinese + English headers as shown in template). Analysis content can be in Chinese.
- **Date handling**: If exact date is unknown, use the search result's publication date. If unavailable, use today's date with a note.
- **Source credibility**: Prefer authoritative sources (Reuters, Bloomberg, FT, AP, Al Jazeera, Times of Israel, Tehran Times, 新华社, 环球时报). Flag if a source is low-credibility or state-aligned propaganda.
- **Scope**: Focus on events with material geopolitical or market relevance — military strikes, nuclear talks, sanctions, diplomatic breakthroughs/breakdowns, proxy conflict escalations. Avoid minor social media speculation or unverified rumors.
- **Oil price sensitivity**: Always assess Strait of Hormuz risk — if threatened, note ~20% of global seaborne oil passes through it. This is the primary transmission mechanism to energy markets.
- **Deduplication priority**: When in doubt, skip. It is better to miss a duplicate than to re-analyze the same event twice.
