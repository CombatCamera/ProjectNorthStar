# Project NorthStar Financial Standard

**Version:** 1.0  
**Status:** Approved  
**Last Updated:** 2026-08-18

---

## Purpose

The NorthStar Financial Standard defines the official monetary calculation
rules for every component of the NorthStar platform.

Its purpose is to ensure that all monetary calculations remain deterministic,
auditable, and consistent across the Generation Engine, QA Engine, Training
Population Generator, Privacy Engine, Feature Engineering, Machine Learning
pipelines, and future NorthStar Live services.

This standard eliminates floating-point precision errors and establishes a
single authoritative monetary calculation policy for the platform.

## Scope

This standard applies to every NorthStar component that creates, modifies,
validates, or consumes monetary values.

This includes:

- Generation Engine
- QA Engine
- Training Population Generator
- Feature Engineering
- Machine Learning datasets
- Privacy Engine when processing monetary fields
- Future NorthStar Live services

---

## Engineering Principles

The NorthStar Financial Standard follows these architectural principles:

1. Monetary calculations must be deterministic.
2. Every engine must produce identical financial results given identical inputs.
3. Monetary calculations must never depend on binary floating-point behavior.
4. QA validates compliance with this standard rather than implementing
   independent financial rules.
5. Financial calculations should remain simple, maintainable, and teachable.


## Monetary Representation

### Standard

All monetary calculations must use Python's `Decimal` type.

Binary floating-point (`float`) must not be used for financial calculations.

### Rationale

`Decimal` provides exact decimal arithmetic appropriate for currency
calculations and prevents binary floating-point precision artifacts from
affecting NorthStar's financial values.

---

## Monetary Precision

All stored monetary values must be rounded to two decimal places.

This includes, but is not limited to:

- `UnitPrice`
- `UnitCost`
- `LineTotal`
- `Subtotal`
- `DiscountAmount`
- `Shipping`
- `Tax`
- `Total`
- `PaymentAmount`

Fractions of a cent must not propagate into downstream monetary calculations.

## Rounding Method

NorthStar uses `ROUND_HALF_UP` for all monetary rounding.

### Examples

| Calculated Value | Stored Value |
| ---------------: | -----------: |
|         `33.915` |      `33.92` |
|         `18.325` |      `18.33` |
|         `14.994` |      `14.99` |

All monetary values requiring rounding must follow this policy consistently.

## Calculation Order

Every order must be calculated in the following sequence:

<div align="center">
<pre>
Subtotal
↓
Discount
↓
Round Discount
↓
Discounted Subtotal
↓
Shipping
↓
Tax
↓
Round Tax
↓
Final Total
↓
Round Final Total
</pre>
</div>

Each monetary stage becomes the authoritative value for all subsequent calculations.

## Monetary Rounding Utility

All NorthStar components that perform monetary rounding must use the
`round_currency()` function.

Every implementation of `round_currency()` must apply the same financial
standard:

- Convert monetary values to `Decimal`.
- Quantize values to `Decimal("0.01")`.
- Use `ROUND_HALF_UP` rounding.

Components must not introduce independent monetary rounding rules.

---

## QA Certification

The QA Engine must reproduce the same monetary calculation and rounding rules
used by the Generation Engine.

QA exists to verify compliance with the NorthStar Financial Standard, not to
define an alternative financial calculation policy.

Financial QA must validate that generated monetary values reconcile according
to the approved representation, precision, rounding method, and calculation
order.

## Design Philosophy

NorthStar follows a simple rule for financial logic:

> **Define the standard once. Implement it consistently everywhere.**

Financial rules are platform-wide standards.

Individual engines and components may implement the calculations required for
their responsibilities, but they must not redefine NorthStar's monetary
representation, precision, rounding method, or calculation rules.

This keeps financial behavior deterministic, auditable, maintainable, and
consistent throughout the platform.

---

## Version History

| Version | Date       | Description                                                                                                                 |
| ------- | ---------- | --------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | 2026-08-18 | Established the NorthStar Financial Standard using `Decimal`, two-decimal precision, and `ROUND_HALF_UP` monetary rounding. |