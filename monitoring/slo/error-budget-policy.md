# Robot Shop Availability and Error-Budget Policy

Owner: Chiedozie Friday
Scope: TS Academy Capstone 2 laboratory

## Objective and measurement

The Robot Shop homepage should pass at least 99.5% of scheduled
availability checks over a rolling 24-hour window. Blackbox Exporter
checks http://web.robot-shop.svc.cluster.local:8080/ every 30 seconds.
A successful check returns HTTP 2xx within five seconds, including
any redirects.

This SLO measures homepage reachability from inside Kubernetes.
It does not establish external internet access, successful checkout,
or availability of every microservice.

Availability = successful checks / completed checks × 100.
Error-budget consumption = failed checks / completed checks / 0.005 × 100.

## Budget and data quality

The error budget is 0.5% failed checks. With 2,880 checks in a complete
24-hour window, at most 14 failed checks meet the objective. This is
approximately seven minutes of sampled unavailability, rather than
an exact measurement of continuous downtime.

Report windows shorter than 24 hours as provisional. Missing checks
are unknown, never successes. If monitoring gaps occur, show the
observed availability and disclose incomplete coverage; do not
claim the full-window SLO was met until coverage is established.

## Response and release decisions

A continuously failing probe alerts #capstone-alerts after two minutes.
Missing probe results trigger a separate monitoring alert after
approximately three minutes. These alerts require Prometheus and
Alertmanager themselves to remain operational.

The owner acknowledges alerts within five minutes during attended
lab sessions. Restore service first using a known-good configuration
or rollback, then investigate with metrics, logs, traces, and events.

When more than half the budget is consumed, prioritize reliability
work and review planned changes. When the budget is exhausted,
pause feature changes; permit recovery and security fixes. Resume
feature changes once a complete rolling window meets the objective
and recovery is verified.

## Review and incident evidence

Review availability and coverage daily during the project. Record
incident start, detection, mitigation, recovery, impact, root cause,
and corrective actions. Instructor-triggered application failures
remain part of the measured results. Document the drill honestly
and retain screenshots and the postmortem in the repository.
