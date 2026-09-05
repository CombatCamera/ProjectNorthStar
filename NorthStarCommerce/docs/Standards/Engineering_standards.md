# Project NorthStar Engineering Standards

## Purpose

This document records approved engineering standards and implementation
decisions used throughout Project NorthStar.

These standards provide a consistent reference for how recurring technical
decisions should be handled across NorthStar's engines, utilities, QA systems,
and future development.

The goal is not to document every implementation detail. It is to preserve
decisions that should remain consistent across the project.

## NS-001 — Numeric Types

**Status:** Approved

### Standard

Use `Decimal` for all currency values.

Use `float` for non-currency mathematical calculations, including:

- Averages
- Rates
- Percentages
- Statistics
- Machine learning features

Use `int` for counts and whole-number quantities.

### Rationale

Different numeric types serve different purposes within NorthStar.

Currency requires predictable decimal arithmetic and must not rely on
binary floating-point behavior. Non-currency analytical calculations
may use floating-point arithmetic, while counts and whole-number
quantities should remain integers.

## NS-002 — Financial Calculations

**Status:** Approved

### Standard

All monetary calculations must comply with the
[NorthStar Financial Standard](Financial_Standard.md).

The Financial Standard is the authoritative source for:

- Monetary representation
- Currency precision
- Rounding behavior
- Calculation order
- Shared monetary utilities
- Financial QA requirements

Financial rules should not be independently redefined within this document.


## FE-001 — Insufficient History Policy

**Status:** Approved

### Standard

When a behavioral feature cannot be calculated because the customer does not
have sufficient purchase history, return `NaN`.

Do not replace insufficient-history values with `0` or another sentinel value.

### Rationale

`NaN` preserves the distinction between:

- A legitimate calculated value of zero
- A value that cannot yet be calculated because sufficient evidence does not exist

This approach:

- Preserves the semantic meaning of the feature
- Follows native Pandas missing-value behavior
- Avoids artificial sentinel values
- Remains compatible with downstream machine learning workflows

## Engineering Principles

### Simplicity, Clarity, and Teachability

Prefer the simplest design that remains clear, maintainable, and teachable.

NorthStar should favor explicit, understandable implementations over clever
or unnecessarily complex solutions.

Code should make its intent easy to understand, maintain, explain, and verify.

### Explicit and Readable Code

Prefer explicit, readable statements that make the intended behavior clear.

NorthStar should favor code that reads naturally and communicates its purpose
over abbreviated, clever, or implicit syntax, even when the shorter approach
is idiomatic.

Clarity, maintainability, and teachability take priority over saving
characters.

## Maintaining These Standards

Engineering standards should be added or changed only when NorthStar establishes
a reusable technical decision that should remain consistent across future
development.

Standards should not duplicate business rules, architecture documentation, or
implementation-specific details maintained elsewhere in the project.

When an approved standard changes, the affected code, QA, and documentation
should be reviewed together to preserve consistency.

## NorthStar Engineering Tradition — DELL YEAH!

**DELL YEAH!** is Project NorthStar's unofficial engineering celebration.

It originated during NorthStar's development and became the traditional
response to successful builds, completed milestones, solved problems, and
those particularly satisfying moments when the system finally behaves exactly
as intended.

It has no technical authority, imposes no engineering requirement, and
provides absolutely no QA certification whatsoever.

Its purpose is considerably more important:

Celebrate the win.

**DELL YEAH!**