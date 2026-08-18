Issue #001 – Financial Rounding Policy

Status: Open

Priority: Low

Discovered In: QA Engine v2.0 validation of Training Population

Description

QA Engine v2.0 identified a reproducible floating-point rounding edge case during order total reconciliation.

Dataset: Training Population
OrderID: 15402
Frequency: 1 occurrence in 77,382 orders
Operational dataset: No occurrences observed
Root Cause

NorthStar currently does not have a formally defined financial rounding policy.

The Generation Engine and QA Engine perform mathematically equivalent calculations, but binary floating-point precision can produce rare half-cent boundary differences.

Impact
Prevents certification of an otherwise valid dataset.
No evidence of incorrect business logic.
Indicates a need for a standardized monetary arithmetic policy.
Proposed Resolution
Evaluate using Python's Decimal type for currency calculations.
Define a canonical financial rounding policy.
Apply the same policy consistently across:
Generation Engine
QA Engine
Future Feature Engineering
Machine Learning datasets
Notes

QA Engine diagnostic reporting successfully isolated the issue, demonstrating that the new QA diagnostic capabilities are functioning as designed.