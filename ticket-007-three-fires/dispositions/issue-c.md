# Issue C — Internet-Facing Portal

## Final Classification
Operational Issue with Security Follow-Up

## Evidence
- Portal experienced intermittent HTTP 500 errors.
- Operations had recently deployed a configuration change.
- Errors returned toward baseline after rollback.
- Unusual web requests continued after service recovery.
- Available timing evidence did not show that the unusual requests caused the degradation.

## Confidence
Moderate to high that the service degradation was caused by the configuration change.

## Security Impact
No confirmed portal compromise. Continued unusual internet traffic requires routine security review.

## Business Impact
Temporary customer-facing service degradation and increased support activity.

## Actions Taken
Preserved relevant logs, compared unusual traffic with errors, advised Operations not to delay rollback, and continued lower-priority security review.

## Remaining Actions
Monitor unusual requests and investigate further if exploit indicators or abnormal application behavior appear.

## Owner
IT Operations for service stability; SOC for security monitoring.

## Closure Criteria
Portal remains stable after rollback and ongoing traffic review shows no evidence of successful exploitation.
