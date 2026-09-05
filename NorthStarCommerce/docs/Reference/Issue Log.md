# Issue Log

## Issue #001 – Financial Rounding Policy

**Status:** Resolved

**Priority:** Low

**Discovered In:** QA Engine v2.0 validation of Training Population

---

### Description

QA Engine v2.0 identified a reproducible floating-point rounding edge case during order total reconciliation.

**Dataset:** Training Population  
**OrderID:** 15402  
**Frequency:** 1 occurrence in 77,382 orders  
**Operational Dataset:** No occurrences observed

The affected order produced a half-cent boundary condition where mathematically equivalent calculations could produce different results when represented using binary floating-point arithmetic.

---

### Root Cause

NorthStar did not yet have a formally defined financial rounding policy.

The Generation Engine and QA Engine performed mathematically equivalent calculations, but binary floating-point representation could produce rare differences at currency rounding boundaries.

The issue was therefore determined to be a monetary arithmetic standardization problem rather than incorrect business logic.

---

### Impact

The issue prevented QA certification of an otherwise valid training dataset.

No evidence of corrupted source data or incorrect order-total business logic was identified.

The issue demonstrated that monetary calculations required a single canonical arithmetic and rounding standard across NorthStar.

---

### Resolution

NorthStar adopted a canonical financial arithmetic policy for currency calculations.

The standard is:

```text
Arithmetic Type: Decimal
Currency Precision: 0.01
Rounding Method: ROUND_HALF_UP
```
Currency values are quantized to two decimal places using the shared `round_currency()` policy.


The same financial standard is used by generation and QA logic so that monetary calculations and their validation follow identical rounding rules.

The policy also applies to downstream monetary feature calculations where currency rounding is required.

## Historical Note — Order 15402

Issue #001 began with a single failed QA record: Order 15402.

What initially appeared to be a minor floating-point precision mismatch exposed
a larger architectural question: NorthStar did not yet have a formally defined
financial calculation standard.

Investigating that record ultimately led to the adoption of `Decimal`,
`ROUND_HALF_UP`, the shared `round_currency()` policy, formal financial
engineering standards, and consistent financial validation across the
Generation and QA Engines.

Following implementation, the operational dataset was regenerated and
successfully passed all 18 QA validations, including financial reconciliation.

Order 15402 therefore remains part of NorthStar's engineering history as an
example of why individual QA failures should be investigated rather than
simply suppressed.

---
<div align="center">

### In Memory of Order 15402

**R.I.P.**  
**ORDER 15402**  
*2026–2026*

*Found 0.005.*  
*Changed an architecture.*  
*Rounded in peace.*

🌹

</div>

---

### Verification

Following implementation of the financial rounding standard, the previously identified reconciliation edge case no longer prevented dataset certification.

The Generation Engine and QA Engine were able to evaluate monetary values using the same canonical financial policy.

---

### Engineering Outcome

Issue #001 resulted in NorthStar establishing an explicit financial arithmetic standard rather than applying a one-off correction to the affected order.

This preserves consistent monetary behavior across current and future NorthStar components.

---

### Historical Note

QA Engine diagnostic reporting successfully isolated the original mismatch to `OrderID 15402`.

The issue demonstrated the value of diagnostic QA output: rather than merely reporting a failed reconciliation check, the QA system exposed the specific values required to identify the underlying floating-point boundary condition.