---
name: project-evaluation-agent
description: Perform post-project financial calculations (etterkalkyle), analyze baseline deviations, and compile cost benchmarks to improve future bidding models.
---

# Skill: Project Evaluation & Post-Calculation Agent

This skill guides the agent in conducting post-project financial audits (*etterkalkyle*), identifying root causes of baseline deviations, and summarizing organizational learning.

## When to Use
Activate this skill when:
* Conducting closeout reviews on completed projects (e.g. at stage gates or project end).
* Performing variance analysis comparing original baseline budget (`BAC`) to Final Actual Cost (`FAC`).
* Compiling lessons-learned reports and cost-driver benchmarks.
* Preparing feed-forward data for future bidding and estimating teams.

## Role Directives & Rules
1. **Variance Decomposition**: Deconstruct total cost overruns into specific drivers:
   * *Labor Rate Variance*: Higher standard rates than planned.
   * *Labor Efficiency Variance*: More hours worked than planned.
   * *Material Price Variance*: Higher material costs per unit.
   * *Material Quantity Variance*: More materials consumed than planned.
2. **Closeout report Format**: Output standard summaries including BAC, Final AC, Variance, and a list of top 3 cost-saving or cost-overrunning items.
3. **Lessons Learned Database**: Log specific root causes (e.g., "Composite cure times took 20% longer than vendor spec due to shop-floor temp issues") to update the PM's planning guidelines.
4. **Bidding Database Update**: Extract actual unit costs (e.g., "Average cost per ton of structural steel was X NOK") to update the estimating team's pricing databases.
