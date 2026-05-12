# Architecture

Learner Intervention Ledger is the outcome and audit layer for higher-ed intervention workflows.

## Inputs

- Intervention event type
- Owner lane
- Channel
- Status
- Outcome
- Days open
- Touch count
- Response received
- Risk shift
- Escalation level

## Core idea

Most student-success tools stop at “a case exists.” This repo extends that into:

- whether the outreach sequence is working
- whether the case is stuck
- which lanes are overloaded
- which closed cases represent reusable patterns

## Outputs

- Dashboard summary
- Intervention ledger
- Outcome-quality breakdown
- Lane workload breakdown
- Case evidence view
- API payloads for dashboards and CRMs
