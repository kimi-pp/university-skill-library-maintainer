---
name: uk-tax-calculation
description: Calculate UK income tax, National Insurance and take-home pay for employees, the self-employed, contractors and people moving to or from the UK. Use this whenever someone asks what they will take home on a UK salary, how a London or Edinburgh offer compares, what their effective or marginal rate is, why a pay rise left them barely better off, how Scottish rates differ, what a bonus costs them, how much a sole trader owes, or how pension contributions or salary sacrifice change the result — including when they only mention PAYE, a payslip, or HMRC.
---

# UK income tax and National Insurance calculation — tax year 2025/26

Read `references/calculation-workflow.md` for the general method. This file
covers what is specific to the United Kingdom.

## Run the engine

```bash
python -m taxcalc calc GB --employment 65000
python -m taxcalc calc GB --employment 110000            # the taper zone
python -m taxcalc calc GB --employment 90000 --region SCT   # Scottish rates
python -m taxcalc calc GB --self-employment 70000
python -m taxcalc info GB
```

## Establish these before computing

- **The tax year is 6 April to 5 April.** Anyone arriving from a calendar-year
  country will assume otherwise. Confirm which year they mean before quoting a
  figure.
- **Scotland or the rest of the UK.** Scottish taxpayers have six bands reaching
  48%, and the divergence at 50,000–125,000 of income is several thousand pounds
  a year. Pass `--region SCT`.
- **Pension arrangement.** Salary sacrifice reduces both income tax and NI and
  is materially better than relief at source. If they mention a pension at all,
  ask which one — it changes the answer more than almost anything else.

## The 100,000–125,140 trap

Between these figures the personal allowance is withdrawn at £1 for every £2,
producing a **60% effective marginal rate** (63% in Scotland). Add the loss of
free childcare hours and tax-free childcare, which cut off hard at 100,000 of
adjusted net income, and the effective rate for a parent of young children can
exceed 100%.

The engine shows this in the marginal wedge. Whenever income lands in or near
this band, point it out and mention that a pension contribution bringing
adjusted net income below 100,000 is relieved at that same 60%. This is the most
valuable single piece of UK tax planning for ordinary earners and most people
have never had it explained.

## Other UK specifics worth raising

- **High Income Child Benefit Charge** claws back child benefit between 60,000
  and 80,000, assessed on the higher earner. It catches households who never
  claimed to be high earners.
- **Most employees never file.** PAYE settles the liability. See the reporting
  skill for what triggers Self Assessment.
- **The remittance basis ended on 6 April 2025**, replaced by the four-year
  foreign income and gains regime for new arrivals. Guidance written before 2025
  is now wrong; say so if the user is working from it.
- **IR35 / off-payroll working** determines whether a contractor is taxed as an
  employee. If someone describes contracting through a limited company, this is
  usually the real question underneath.

## What the engine leaves out

Savings and dividend income use separate rates and allowances that are not
applied. Student loan repayments (9% above the plan threshold) are not included
and are a real cost for younger workers. Pension relief must be handled by
reducing gross income or using `--deductions`.
