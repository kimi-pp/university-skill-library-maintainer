# Generate Briefing Skill

## Description

Creates an automated "CEO Briefing" or daily/weekly report by analyzing vault activities, completed tasks, financial transactions, and key metrics.

## What This Skill Does

1. **Collects** data from multiple vault folders
2. **Analyzes** completed tasks and achievements
3. **Reviews** financial transactions and patterns
4. **Identifies** bottlenecks and opportunities
5. **Generates** a formatted briefing document
6. **Updates** Dashboard with key insights

## Usage

Use this skill for:
- Daily morning briefings
- Weekly business reviews
- Monthly financial audits
- Custom period summaries
- Executive reporting

## Example Commands

```bash
# Generate today's briefing
/generate-briefing

# Generate weekly briefing
/generate-briefing --period weekly

# Generate with specific date range
/generate-briefing --from 2026-02-10 --to 2026-02-17

# Include financial analysis
/generate-briefing --include-financials
```

## Input Data

Reads from:
- `/Done/` - Completed tasks this period
- `/Accounting/` - Financial transactions
- `/Plans/` - Planned work
- `Dashboard.md` - Previous status
- `Business_Goals.md` - Goals and metrics

## Output Format

Creates `/Briefings/YYYY-MM-DD_Briefing.md`:

```yaml
---
generated: 2026-02-17T07:00:00Z
period: daily | weekly | monthly
type: ceo_briefing
---

# CEO Briefing - Week of Feb 17, 2026

## Executive Summary
[1-2 sentence summary of key highlights]

## Key Metrics
- Revenue: $X
- Tasks Completed: Y
- Health: 100%

## Achievements
[List of completed items]

## Bottlenecks
[Any delays or issues]

## Upcoming
[Next important items]

## Recommendations
[Proactive suggestions]
```

## Safety Features

- **Read-only** - No modifications to core files
- **Time-stamped** - Every briefing dated and versioned
- **Audit trail** - Can track changes over time
- **Data validation** - Confirms data before analysis

## Examples

### Daily Briefing
```
Revenue today: $0
Tasks completed: 0
System health: ✅ 100%
No alerts
```

### Weekly Briefing
```
Revenue this week: $0
Tasks completed: 0
Key focus: System setup and initialization
Suggestions: Begin processing first test tasks
```

### Monthly Briefing
With financial data:
```
Monthly revenue: $0
Monthly expenses: $X (setup costs)
Subscription audit: None due yet
Recommendations: Review all tool licenses monthly
```

## Customization

Add metrics to `Business_Goals.md`:

```yaml
---
last_updated: 2026-02-17
review_frequency: weekly
---

## Key Metrics to Track
| Metric | Target | Alert |
|--------|--------|-------|
| Revenue | $10,000 | <80% |
| Response Time | <24h | >48h |
```

## Related Skills

- [`process-inbox`](../process-inbox/SKILL.md) - Process tasks
- [`manage-approvals`](../manage-approvals/SKILL.md) - Handle approvals

## Requirements

- Obsidian vault with proper folder structure
- `Business_Goals.md` file (optional but recommended)
- Claude Code with file reading access
- Completed task files in `/Done/`
