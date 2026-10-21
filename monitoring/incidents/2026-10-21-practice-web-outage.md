# Robot Shop Web Availability: Practice-Drill Postmortem

Date: 21 October 2026
Owner: Chiedozie Friday
Status: Recovered
Exercise: Self-run practice; instructor-led drill remains outstanding

## Summary

Two controlled practice outages tested homepage availability monitoring
and recovery. The fault was deliberately introduced by scaling the web
deployment from one replica to zero.

The first attempt entered Pending and recovered without a recorded
Firing state. The second attempt held the fault for four minutes.
Prometheus detected the failure, Alertmanager delivered the real
availability alert to Slack, and the script restored one web replica.
Kubernetes readiness, a successful homepage probe, and a resolved
Slack notification confirmed recovery.

## Impact

The Robot Shop homepage was unavailable while web had no replicas.
The availability probe returned zero during both outages.

Only the web deployment was deliberately changed. This exercise does
not establish the number of affected users, lost requests, or the
availability of every downstream service.

## Timeline

Times are UTC unless stated otherwise.

| Event | Evidence |
| --- | --- |
| First attempt restoration started: 21:28:02Z | Terminal output |
| First attempt rollout ready: 21:28:06Z | Terminal output |
| First attempt alert entered Pending | Prometheus ALERTS history |
| Second attempt started: 21:49:50Z | Script output |
| Real Slack firing notification: approximately 21:52Z | Slack shows 22:52 Lagos time; seconds unavailable |
| Replacement web pod created and ready: 21:53:50Z | Kubernetes pod timestamps |
| Homepage probe returned to one | Grafana recovery screenshot |
| Resolved notification verified | Slack screenshot captured at 22:57 Lagos time; exact delivery time not recorded |

The second attempt's recorded start-to-pod-readiness interval was
four minutes. This includes the deliberately scheduled waiting period;
it is not a measure of an operator's response speed. Exact continuous
HTTP outage duration requires the underlying probe timestamps.

## Cause and supporting evidence

The injected configuration change set deployment/web replicas to zero.
With no web pods available, the Service could not serve the homepage.

Kubernetes deployment events recorded the ReplicaSet scaling from one
to zero, then zero to one. Restoring the replica count brought the
homepage probe back to one. No application code or image rollback
was needed.

The trigger was known in advance. This was not a blind root-cause
investigation or an instructor-triggered fault.

## Detection and alerting

Blackbox Exporter probed the homepage every 30 seconds. The
RobotShopHomepageUnavailable rule required continuous failure for
two minutes before firing. Alertmanager routed the alert to
#capstone-alerts.

The first attempt produced Pending samples but no Firing samples
in the inspected history, consistent with recovery before the
waiting period elapsed. The second attempt verified both Firing
and Resolved delivery.

Historical max_over_time(ALERTS[1h]) results remain visible after
recovery and must not be interpreted as current alert state.

## Mitigation and recovery

The second attempt used a bounded script with an EXIT restoration
handler. It restored the original replica count after four minutes
and waited for deployment readiness.

Recovery evidence:
- deployment/web returned to one available replica.
- web-6957797cd7-xdgc8 became Ready at 21:53:50Z.
- The new pod initially had zero restarts.
- probe_success returned to one.
- Slack received the resolved availability notification.

## Lessons and follow-up

| Action | Owner | Status |
| --- | --- | --- |
| Use 30-second dashboard refresh during drills | Chiedozie Friday | Completed |
| Retain bounded fault duration and restoration handler | Chiedozie Friday | Demonstrated |
| Preserve probe, Slack, and terminal evidence in the repository | Chiedozie Friday | Pending |
| Review post-drill availability and budget consumption | Chiedozie Friday | Completed |
| Complete the instructor-led drill and document it separately | Chiedozie Friday | Pending |

Keep the two-minute alert threshold unless later evidence justifies
changing it. Restore service before prolonged diagnosis.

Both practice outages consume the measured error budget. The earlier
100% availability result was a pre-drill baseline, not the post-drill
result. Calculate the final budget impact from observed probe samples,
including both attempts.

## Measured post-drill results

Grafana screenshots captured around 23:05 Africa/Lagos on
21 October 2026 showed:

- Rolling 24-hour availability: approximately 99.6181%.
- Availability objective: 99.5%.
- Error budget consumed: approximately 76.39%.
- Error budget remaining: approximately 23.61%.

The observed availability remained above the objective. Both practice
outages contributed to budget consumption. Because more than half the
budget was consumed, the policy calls for prioritizing reliability work.
These are historical measurements; rolling-window values change over time.
