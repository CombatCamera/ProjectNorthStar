Project NorthStar
NorthStar Financial Standard

Version: 1.0

Status: Approved

Last Updated: 2026-08-18

Purpose

The NorthStar Financial Standard defines the official monetary calculation rules for every component of the NorthStar platform.

Its purpose is to ensure that all monetary calculations remain deterministic, auditable, and consistent across the Generation Engine, QA Engine, Training Population Generator, Privacy Engine, Feature Engineering, Machine Learning pipelines, and future NorthStar Live services.

This standard eliminates floating-point precision errors and establishes a single authoritative monetary calculation policy for the platform.

Scope

This standard applies to every component that creates, modifies, validates, or consumes monetary values.

Examples include:

Generation Engine
QA Engine
Training Population Generator
Feature Engineering
Machine Learning datasets
Privacy Engine (when processing monetary fields)
Future NorthStar Live services
Engineering Principles

The Financial Standard follows the following architectural principles:

Monetary calculations must be deterministic.
Every engine shall produce identical financial results given identical inputs.
Monetary calculations shall never depend upon floating-point behavior.
QA validates compliance with this standard rather than implementing independent financial rules.
Financial calculations shall remain simple, maintainable, and teachable.
Monetary Representation
Standard

All monetary calculations shall use Python's Decimal type.

Binary floating-point (float) shall not be used for financial calculations.

Rationale

Decimal provides exact decimal arithmetic appropriate for currency calculations and eliminates binary floating-point precision artifacts.

Monetary Precision

All stored monetary values shall be rounded to two decimal places.

This includes, but is not limited to:

UnitPrice
UnitCost
LineTotal
Subtotal
DiscountAmount
Shipping
Tax
Total
PaymentAmount

Fractions of a cent shall not propagate into downstream monetary calculations.

Rounding Method

NorthStar uses:

ROUND_HALF_UP

for all monetary rounding.

Examples:

Value	Stored
33.915	33.92
18.325	18.33
14.994	14.99
Calculation Order

Every order shall be calculated in the following sequence:

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

Each monetary stage becomes the authoritative value for all subsequent calculations.

Shared Monetary Utility

All monetary rounding shall be performed through the shared utility:

round_currency()

Individual components shall not implement independent rounding logic.

Future changes to monetary precision or rounding behavior shall be implemented within this shared utility.

QA Certification

The QA Engine shall reproduce the exact monetary calculations defined by this standard.

QA exists to verify compliance with the Financial Standard rather than to implement alternative financial calculations.

Generation Engine and QA Engine shall always follow identical monetary rules.

Design Philosophy

The NorthStar Financial Standard reflects the broader architectural philosophy of Project NorthStar:

Define the standard once. Implement it everywhere.

Business rules shall exist as shared platform standards rather than duplicated logic across independent components.

Version History
Version	Date	Description
1.0	2026-08-18	Initial Financial Standard established. Adopted Decimal, ROUND_HALF_UP, shared monetary utility, and standardized calculation order across the Generation Engine and QA Engine.