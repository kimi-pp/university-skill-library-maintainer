---
name: finyx-home
description: |
  Home Assistant sensor integration bridge — air quality, humidity, temperature,
  sleep, weight, and blood pressure data correlated with health diary entries.
  Uses ha-mcp (user-side uvx install) as the sole MCP boundary via
  finyx-home-sensor-agent.

  Sub-skills: setup (one-time HA config), snapshot (current sensor state),
  audit (30/90-day environmental history), correlate (sensor vs. symptom
  cross-correlation as HYPOTHESES).

  Use when the user asks about: Home Assistant, HA sensor data, air quality
  correlation, sleep environment analysis, indoor humidity, CO2, PM2.5, VOC,
  allergen exposure tracking, sensor staleness, environmental audit, correlate
  sensors with symptoms.

  Does NOT cover: medical diagnosis, clinical advice, automated home control,
  non-health sensor analytics. Sibling skill finyx-health covers symptoms,
  records, and clinical preparation. All sensor-symptom correlations are
  HYPOTHESES — never causal claims.

  Prerequisites: ha-mcp installed (see README.md). HOMEASSISTANT_TOKEN env var
  set to a Long-Lived Access Token. finyx-home setup run once.
allowed-tools:
  - Read
  - Write
  - Bash
  - Task
  - AskUserQuestion
---

## Prerequisites

This skill requires **ha-mcp** installed on the user's machine.

```bash
claude mcp add --transport stdio home-assistant \
  --env HOMEASSISTANT_TOKEN=<your-llat> \
  -- uvx ha-mcp
```

See `skills/home/README.md` for full setup instructions including 1Password
LLAT storage, GDPR posture, and the MDR/HeilprG disclaimer.

The `finyx-home-sensor-agent` is the **sole MCP boundary**. This SKILL.md and
all sub-skills invoke the agent via the Task tool and NEVER call ha-mcp directly.

<objective>
Route the user's request to the appropriate finyx-home sub-skill.

This skill:
1. Detects sub-skill type from `$ARGUMENTS` or user input
2. Validates prerequisites (config file, env var)
3. Loads and executes the matched sub-skill
</objective>

<process>

## Phase 0: Type Detection

Inspect `$ARGUMENTS` (case-insensitive) and map to `sub_skill_type`:

| Keyword(s) | sub_skill_type |
|------------|---------------|
| "setup", "configure", "config", "connect", "einrichten" | setup |
| "snapshot", "current", "now", "aktuell", "status", "reading" | snapshot |
| "audit", "history", "30 day", "90 day", "verlauf", "trend" | audit |
| "correlate", "correlation", "symptom", "pattern", "zusammenhang" | correlate |

If not matched or `$ARGUMENTS` is empty: default `sub_skill_type = "snapshot"`.

> Sub-skills available in Phase 31: setup, snapshot, audit, correlate.
> Phase 32 adds the diary overlay integration.

## Phase 1: Sub-Skill Dispatch

```bash
SUB_SKILL_FILE="${CLAUDE_SKILL_DIR}/sub-skills/${sub_skill_type}.md"
if [ ! -f "$SUB_SKILL_FILE" ]; then
  echo "Sub-skill '${sub_skill_type}' not found. Available: setup, snapshot, audit, correlate"
  exit 1
fi
```

Load and execute the matched sub-skill. The sub-skill handles all subsequent
phases including prerequisite validation, sensor-agent spawning, and output.
</process>

## Legal Disclaimer

All sensor-symptom correlations produced by this skill are framed as **hypotheses**,
not causal claims. Finyx Home is NOT a medical device under EU MDR Art. 2(1), NOT
licensed Heilkunde under HeilprG, and does NOT provide medical advice.

Environmental threshold exceedances (humidity, PM2.5, CO2, VOC) are reference
values from UBA, WHO, and AWMF — not diagnostic criteria.

See `../health/references/legal/disclaimers.md` for the canonical HeilprG
safe-harbor text. Sub-skills that display output referencing health thresholds
MUST include the disclaimer block from that file.

**Emergency: 112 | Non-emergency medical: 116117 | Mental health: 0800 111 0 111**
