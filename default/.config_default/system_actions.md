# Arboris System Action IDs
| ID | Name | Description | Required Payload |
|:---|:---|:---|:---|
| 0 | Chat | Standard technical dialogue. | None (null) |
| 1 | Branch | Splitting current node into new paths. | `summary`, `alternatives` |
| 2 | Investigate | Mandatory failure analysis. | None (null) |
| 3 | Inactivate | Permanent closure of the node. | `inactivation_report` |