# NorthStar Commerce
## Data Dictionary

Version 1.1

---

# Overview

This document defines the structure, purpose, and business meaning of the primary data used throughout NorthStar Commerce.

NorthStar Commerce contains two distinct data layers:

* **SQL Server Data** — the operational business data generated and stored within the NorthStar Commerce relational database.
* **Python Data** — the analytical, feature-engineering, historical machine learning, and prediction data produced from approved NorthStar business data.

These layers are documented separately to preserve a clear distinction between source business records and the derived data created for analytics and machine learning.

---

# Part I — SQL Server Data Dictionary

This section documents the operational tables stored within the NorthStar Commerce SQL Server database.

It includes:

* Table purpose
* Column names
* SQL data types
* Business meaning
* Primary and foreign key relationships

The SQL Server database represents the underlying business entities and events generated within the NorthStar Commerce synthetic e-commerce environment.

---

# Table: Categories

## Purpose

Stores the product categories available throughout NorthStar Commerce.

## Grain

One row per product category.

| Column       | Data Type    | Description                                             |
| ------------ | ------------ | ------------------------------------------------------- |
| CategoryID   | TINYINT      | Unique identifier for each product category.            |
| CategoryName | NVARCHAR(50) | Human-readable category name used to classify products. |

## Relationships

**Primary Key**

`CategoryID`

**Referenced By**

`Products.CategoryID`

# Table: Customers

## Purpose

Stores demographic information, account attributes, and behavioral characteristics for every customer in NorthStar Commerce. This table represents the master customer record used throughout the enterprise.

## Grain

One row per customer.

| Column          | Data Type    | Description                                                            |
| --------------- | ------------ | ---------------------------------------------------------------------- |
| CustomerID      | SMALLINT     | Unique identifier for each customer.                                   |
| FirstName       | NVARCHAR(50) | Customer's first name.                                                 |
| LastName        | NVARCHAR(50) | Customer's last name.                                                  |
| Email           | NVARCHAR(50) | Customer email address.                                                |
| Phone           | NVARCHAR(50) | Customer phone number.                                                 |
| City            | NVARCHAR(50) | Customer city of residence.                                            |
| State           | NVARCHAR(50) | Customer state of residence.                                           |
| Region          | NVARCHAR(50) | Sales region used for geographic reporting.                            |
| BirthYear       | SMALLINT     | Customer birth year used for demographic analysis.                     |
| Gender          | NVARCHAR(50) | Customer gender.                                                       |
| JoinDate        | DATE         | Date the customer first joined NorthStar Commerce.                     |
| CustomerSegment | NVARCHAR(50) | Business-defined customer segmentation.                                |
| LoyaltyTier     | NVARCHAR(50) | Customer loyalty program tier.                                         |
| ShoppingProfile | NVARCHAR(50) | Simulated purchasing behavior profile assigned during data generation. |
| IsActive        | BIT          | Indicates whether the customer account is currently active.            |

## Relationships

**Primary Key**

`CustomerID`

**Referenced By**

`Orders.CustomerID`

# Table: Products

## Purpose

Stores the product catalog available for purchase within NorthStar Commerce. Each row represents one product and identifies its category, current catalog pricing, launch date, and active status.

## Grain

One row per product.

| Column      | Data Type     | Description                                                  |
| ----------- | ------------- | ------------------------------------------------------------ |
| ProductID   | TINYINT       | Unique identifier for each product.                          |
| CategoryID  | TINYINT       | Identifies the product category associated with the product. |
| ProductName | NVARCHAR(50)  | Human-readable product name.                                 |
| UnitPrice   | DECIMAL(10,2) | Current catalog selling price of the product.                |
| UnitCost    | DECIMAL(10,2) | Current unit cost associated with the product.               |
| LaunchDate  | DATE          | Date the product became available within NorthStar Commerce. |
| IsActive    | BIT           | Indicates whether the product is currently active.           |

## Relationships

**Primary Key**

`ProductID`

**Foreign Key**

`CategoryID` → `Categories.CategoryID`

**Referenced By**

`Order_Items.ProductID`

## Important Business Note

`Products.UnitPrice` represents the current catalog price.

The selling price recorded in `Order_Items.UnitPrice` represents the price captured at the time of purchase. Historical sales analysis should therefore use `Order_Items.UnitPrice` rather than the current product catalog price.

# Table: Orders

## Purpose

Stores customer order-level transaction information within NorthStar Commerce. Each row represents one customer order and records the order timestamp, pricing components, shipping method, and final order total.

## Grain

One row per customer order.

| Column         | Data Type     | Description                                                       |
| -------------- | ------------- | ----------------------------------------------------------------- |
| OrderID        | INT           | Unique identifier for each order.                                 |
| CustomerID     | SMALLINT      | Identifies the customer who placed the order.                     |
| OrderDateTime  | DATETIME2     | Date and time the order was placed.                               |
| Subtotal       | DECIMAL(10,2) | Order value before discounts, shipping, and tax are applied.      |
| DiscountRate   | DECIMAL(4,2)  | Discount rate applied at the order level.                         |
| DiscountAmount | DECIMAL(10,2) | Monetary value of the discount applied to the order.              |
| ShippingMethod | NVARCHAR(50)  | Shipping method selected for the order.                           |
| Shipping       | DECIMAL(10,2) | Shipping charge applied to the order.                             |
| Tax            | DECIMAL(10,2) | Tax amount applied to the order.                                  |
| Total          | DECIMAL(10,2) | Final order total after discounts, shipping, and tax are applied. |

## Relationships

**Primary Key**

`OrderID`

**Foreign Key**

`CustomerID` → `Customers.CustomerID`

**Referenced By**

`Order_Items.OrderID`

`Payments.OrderID`

`Shipments.OrderID`

## Important Business Notes

Discounts are applied at the order level.

An order may contain multiple products through `Order_Items`.

An order may have multiple payment attempts through `Payments`.

An order may have one or more shipments through `Shipments`.

All monetary values are stored using `DECIMAL(10,2)`.

Because an order may have multiple payment attempts, joining `Orders` directly to `Payments` can duplicate order rows. Completed revenue analysis should use successful payment status appropriately when payment data is included.


# Table: Order_Items

## Purpose

Stores the individual products included within each NorthStar Commerce order. Each row represents one product line within an order and records the quantity purchased, selling price at the time of purchase, and resulting line total.

## Grain

One row per product within an order.

| Column      | Data Type     | Description                                                       |
| ----------- | ------------- | ----------------------------------------------------------------- |
| OrderItemID | INT           | Unique identifier for each order item record.                     |
| OrderID     | INT           | Identifies the order that contains the product line.              |
| ProductID   | TINYINT       | Identifies the product included in the order.                     |
| Quantity    | TINYINT       | Number of units purchased for the product line.                   |
| UnitPrice   | DECIMAL(10,2) | Selling price per unit captured at the time of purchase.          |
| LineTotal   | DECIMAL(10,2) | Total value of the product line based on quantity and unit price. |

## Relationships

**Primary Key**

`OrderItemID`

**Foreign Keys**

`OrderID` → `Orders.OrderID`

`ProductID` → `Products.ProductID`

## Important Business Notes

`Order_Items.UnitPrice` represents the selling price of the product at the time of purchase.

This value should be used for historical sales analysis instead of `Products.UnitPrice`, which represents the product's current catalog price.

An order may contain multiple product lines.

Joining `Orders` to `Order_Items` duplicates the order-level record once for each associated product line, so analysts should account for table grain when aggregating order-level measures.


# Table: Payments

## Purpose

Stores payment attempts associated with NorthStar Commerce orders. Each row represents one payment attempt and records when the attempt occurred, the payment method, payment amount, and resulting payment status.

## Grain

One row per payment attempt.

| Column          | Data Type     | Description                                                 |
| --------------- | ------------- | ----------------------------------------------------------- |
| PaymentID       | INT           | Unique identifier for each payment attempt.                 |
| OrderID         | INT           | Identifies the order associated with the payment attempt.   |
| PaymentAttempt  | TINYINT       | Sequential payment-attempt number for the associated order. |
| PaymentDateTime | DATETIME2     | Date and time the payment attempt occurred.                 |
| PaymentMethod   | NVARCHAR(50)  | Payment method used for the payment attempt.                |
| PaymentAmount   | DECIMAL(10,2) | Monetary amount associated with the payment attempt.        |
| PaymentStatus   | NVARCHAR(50)  | Resulting status of the payment attempt.                    |

## Relationships

**Primary Key**

`PaymentID`

**Foreign Key**

`OrderID` → `Orders.OrderID`

## Important Business Notes

An order may have multiple payment attempts.

Only `PaymentStatus = 'Successful'` represents a completed payment.

NorthStar measures successful customer purchase behavior using orders associated with a successful payment.

Because multiple payment attempts may exist for a single order, joining `Orders` directly to `Payments` can produce multiple rows for the same order. Analysts should account for payment-attempt grain when performing order-level analysis.

# Table: Shipments

## Purpose

Stores shipment records associated with NorthStar Commerce orders. Each row represents one shipment and records the carrier, tracking information, shipment timing, delivery timing, shipment status, delay status, shipping method, and shipping cost.

## Grain

One row per shipment.

| Column                    | Data Type     | Description                                                                            |
| ------------------------- | ------------- | -------------------------------------------------------------------------------------- |
| ShipmentID                | INT           | Unique identifier for each shipment.                                                   |
| OrderID                   | INT           | Identifies the order associated with the shipment.                                     |
| Carrier                   | NVARCHAR(50)  | Shipping carrier responsible for the shipment.                                         |
| TrackingNumber            | NVARCHAR(50)  | Tracking number assigned to the shipment.                                              |
| ShipmentDateTime          | DATETIME2     | Date and time the shipment was created or dispatched.                                  |
| EstimatedDeliveryDateTime | DATETIME2     | Estimated date and time the shipment is expected to be delivered.                      |
| ActualDeliveryDateTime    | DATETIME2     | Actual date and time the shipment was delivered. Remains `NULL` until delivery occurs. |
| ShipmentStatus            | NVARCHAR(50)  | Current status of the shipment.                                                        |
| IsDelayed                 | BIT           | Indicates whether the shipment is classified as delayed.                               |
| ShippingMethod            | NVARCHAR(50)  | Shipping method used for the shipment.                                                 |
| ShippingCost              | DECIMAL(10,2) | Monetary shipping cost associated with the shipment.                                   |

## Relationships

**Primary Key**

`ShipmentID`

**Foreign Key**

`OrderID` → `Orders.OrderID`

## Important Business Notes

An order may have one or more shipments.

`ActualDeliveryDateTime` remains `NULL` until the shipment has been delivered.

`IsDelayed` identifies the shipment's delay status.

All shipment date and time fields use UTC.

Because an order may have multiple shipments, joining `Orders` directly to `Shipments` can produce multiple rows for the same order. Analysts should account for shipment grain when performing order-level analysis.


# Part II — Python Data Dictionary

This section documents the primary Python data structures and derived fields created during NorthStar Commerce analytical and machine learning processing.

It includes data produced through:

* Privacy filtering
* Business Data Preparation
* Feature Engineering
* Business Interpretation
* Historical machine learning dataset generation
* Machine learning development
* Prediction generation

Python-derived data does not replace the operational SQL database. It represents approved transformations, measurements, interpretations, and predictions produced from NorthStar business data for analytical and machine learning purposes.

# Privacy-Filtered Data

## Purpose

The Privacy Engine transforms QA-certified NorthStar datasets into privacy-preserving analytical datasets suitable for downstream analytics, machine learning, predictive modeling, portfolio use, research, and external sharing.

The Privacy Engine removes direct customer and order identifiers, replaces them with dataset-scoped anonymous identifiers, applies customer-scoped temporal offsets, removes fields that have not been explicitly approved, and preserves the business relationships required for downstream processing.

---

## Dataset: Anonymous Customers

### Purpose

Stores the privacy-preserving customer records approved for downstream analytical use.

### Grain

One row per anonymous customer.

| Field                  | Python Representation | Description                                                                                                                             |
| ---------------------- | --------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `AnonymousCustomerKey` | String                | Dataset-scoped UUID that replaces the original `CustomerID` while preserving customer-level relationships across privacy-safe datasets. |
| `JoinDate`             | Date-formatted string | Customer join date after application of the customer-specific temporal offset.                                                          |

### Source

Derived from the NorthStar customer dataset through the Privacy Engine.

### Important Business Notes

`CustomerID` is not retained in the privacy-safe output.

The same temporal offset applied to the customer's other dated events is also applied to `JoinDate`, preserving relative event timing while obscuring the original calendar dates.

---

## Dataset: Anonymous Orders

### Purpose

Stores privacy-preserving order records approved for downstream behavioral feature engineering.

### Grain

One row per anonymous order.

| Field                  | Python Representation       | Description                                                                        |
| ---------------------- | --------------------------- | ---------------------------------------------------------------------------------- |
| `AnonymousOrderKey`    | String                      | Dataset-scoped UUID that replaces the original `OrderID`.                          |
| `AnonymousCustomerKey` | String                      | Anonymous identifier of the customer associated with the order.                    |
| `OrderDateTime`        | Datetime-formatted string   | Order date and time after application of the customer's temporal offset.           |
| `Total`                | String when loaded from CSV | Final order total retained for approved downstream behavioral feature engineering. |

### Source

Derived from the NorthStar order dataset through the Privacy Engine.

### Important Business Notes

`OrderID` and `CustomerID` are not retained in the privacy-safe output.

`Total` is explicitly retained because it is required for downstream behavioral feature engineering, including `AverageOrderValue`.

The customer's temporal offset is applied consistently to the order timestamp.

---

## Dataset: Anonymous Payments

### Purpose

Stores privacy-preserving payment-attempt records while preserving the information required to determine successful purchase behavior.

### Grain

One row per anonymous payment attempt.

| Field               | Python Representation       | Description                                                                                   |
| ------------------- | --------------------------- | --------------------------------------------------------------------------------------------- |
| `AnonymousOrderKey` | String                      | Anonymous identifier of the order associated with the payment attempt.                        |
| `PaymentAttempt`    | String when loaded from CSV | Sequential payment-attempt number associated with the order.                                  |
| `PaymentDateTime`   | Datetime-formatted string   | Payment-attempt date and time after application of the associated customer's temporal offset. |
| `PaymentStatus`     | String                      | Resulting status of the payment attempt.                                                      |

### Source

Derived from the NorthStar payment dataset through the Privacy Engine.

### Important Business Notes

The original `OrderID` is replaced by `AnonymousOrderKey`.

`PaymentStatus` is retained because downstream purchase behavior depends on identifying successful payments.

The same customer-scoped temporal offset used for the related order is applied to the payment timestamp.

---

## Dataset: Anonymous Purchase History

### Purpose

Reconstructs the approved privacy-safe customer, order, and payment relationships into a single analytical purchase-history dataset.

### Grain

One row per payment attempt associated with an anonymous order.

| Field                  | Python Representation       | Description                                                                       |
| ---------------------- | --------------------------- | --------------------------------------------------------------------------------- |
| `AnonymousCustomerKey` | String                      | Anonymous identifier of the customer associated with the purchase history record. |
| `JoinDate`             | Date-formatted string       | Privacy-shifted customer join date.                                               |
| `AnonymousOrderKey`    | String                      | Anonymous identifier of the associated order.                                     |
| `OrderDateTime`        | Datetime-formatted string   | Privacy-shifted order date and time.                                              |
| `PaymentAttempt`       | String when loaded from CSV | Sequential payment-attempt number for the associated order.                       |
| `PaymentDateTime`      | Datetime-formatted string   | Privacy-shifted payment-attempt date and time.                                    |
| `PaymentStatus`        | String                      | Resulting status of the payment attempt.                                          |

### Source

Reconstructed from the Privacy Engine's anonymous customer, order, and payment datasets.

### Important Business Notes

This dataset preserves the relationships required to identify successful purchase behavior without exposing the original customer or order identifiers.

Because an order may have multiple payment attempts, the same `AnonymousOrderKey` may appear on multiple rows.

The Privacy Engine applies customer-scoped temporal offsets consistently across related customer, order, and payment events so relative event relationships are preserved.

# Business Data Preparation

## Purpose

Business Data Preparation creates reusable intermediate business data objects from approved NorthStar data before feature generation begins.

These objects preserve business meaning, centralize reusable logic, and allow downstream feature families to consume already-prepared business evidence rather than recalculating the same relationships independently.

---

## Dataset: Successful Purchase History

### Purpose

Stores successful customer purchases approved for downstream behavioral analysis.

A purchase is included only when its associated payment record has `PaymentStatus = "Successful"`.

### Grain

One row per successful anonymous order.

| Field                  | Python Representation | Description                                                                   |
| ---------------------- | --------------------- | ----------------------------------------------------------------------------- |
| `AnonymousCustomerKey` | String                | Anonymous identifier of the customer associated with the successful purchase. |
| `AnonymousOrderKey`    | String                | Anonymous identifier of the successful order.                                 |
| `OrderDateTime`        | `datetime64`          | Date and time the successful order was placed.                                |
| `Total`                | Numeric               | Final order total associated with the successful purchase.                    |

### Source

Derived by joining the privacy-filtered anonymous order and payment datasets on `AnonymousOrderKey` and retaining only records with successful payment status.

### Important Business Notes

Only successful purchases contribute to downstream customer purchase behavior.

Each successful order is represented only once. Successful payment order keys are deduplicated before joining to the order dataset so multiple successful payment records cannot duplicate a purchase.

`OrderDateTime` is converted to a pandas datetime representation before the dataset is returned.

---

## Dataset: Purchase History As Of Observation Date

### Purpose

Creates the point-in-time purchase history available for a specified evaluation or observation date.

### Grain

One row per successful anonymous order known on or before the applicable observation date.

| Field                  | Python Representation | Description                                                        |
| ---------------------- | --------------------- | ------------------------------------------------------------------ |
| `AnonymousCustomerKey` | String                | Anonymous identifier of the customer associated with the purchase. |
| `AnonymousOrderKey`    | String                | Anonymous identifier of the successful order.                      |
| `OrderDateTime`        | `datetime64`          | Date and time of the successful purchase.                          |
| `Total`                | Numeric               | Final order total associated with the successful purchase.         |

### Source

Derived from `Successful Purchase History`.

### Business Rule

Only records satisfying the following condition are retained:

```text
OrderDateTime <= ObservationDate
```

### Important Business Notes

This dataset establishes NorthStar's point-in-time boundary for historical feature generation.

Purchases occurring after the observation date are excluded so future information cannot influence historical model evidence.

---

## Dataset: Purchase Intervals

### Purpose

Measures the number of days between consecutive successful purchases for each anonymous customer.

### Grain

One row per successful purchase, including the first successful purchase for each customer.

| Field                  | Python Representation | Description                                                                                                   |
| ---------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------- |
| `AnonymousCustomerKey` | String                | Anonymous identifier of the customer associated with the purchase interval record.                            |
| `OrderDateTime`        | `datetime64`          | Date and time of the successful purchase represented by the row.                                              |
| `DaysBetweenPurchases` | Numeric               | Number of whole days between the current successful purchase and the customer's previous successful purchase. |

### Source

Derived from point-in-time successful purchase history.

### Important Business Notes

Records are sorted by `AnonymousCustomerKey` and `OrderDateTime` before intervals are calculated.

The first successful purchase for each customer has no previous purchase for comparison, so `DaysBetweenPurchases` is missing for that row.

Positive values indicate elapsed days between consecutive successful purchases.

---

## Dataset: Purchase Interval Changes

### Purpose

Measures how a customer's consecutive purchase intervals change over time.

### Grain

One row per successful purchase interval record.

| Field                    | Python Representation | Description                                                                                     |
| ------------------------ | --------------------- | ----------------------------------------------------------------------------------------------- |
| `AnonymousCustomerKey`   | String                | Anonymous identifier of the customer associated with the interval-change record.                |
| `OrderDateTime`          | `datetime64`          | Date and time associated with the underlying purchase interval.                                 |
| `DaysBetweenPurchases`   | Numeric               | Number of whole days between consecutive successful purchases.                                  |
| `PurchaseIntervalChange` | Numeric               | Difference between the current purchase interval and the customer's previous purchase interval. |

### Source

Derived from `Purchase Intervals`.

### Calculation

```text
PurchaseIntervalChange =
    Current DaysBetweenPurchases
    - Previous DaysBetweenPurchases
```

### Important Business Notes

A positive `PurchaseIntervalChange` means the customer's purchase interval became longer.

A negative value means the interval became shorter.

A zero value means the interval did not change.

The first available interval change for each customer is missing because no prior interval exists for comparison.

# Feature Engineering

## Purpose

Feature Engineering transforms prepared NorthStar business data into reusable customer-level evidence for analytics, Business Interpretation, historical observation generation, and machine learning.

NorthStar organizes related features into feature families while preserving the principle that every feature answers a defined business question.

---

## Dataset: Temporal Features

### Purpose

Stores customer-level evidence describing purchase timing and current purchase recency.

### Grain

One row per anonymous customer represented in the applicable successful purchase history.

| Field                         | Python Representation | Description                                                                                                     |
| ----------------------------- | --------------------- | --------------------------------------------------------------------------------------------------------------- |
| `AnonymousCustomerKey`        | String                | Anonymous identifier of the customer represented by the feature record.                                         |
| `DaysSinceLastPurchase`       | Numeric               | Number of whole days between the customer's most recent successful purchase and the applicable evaluation date. |
| `AverageDaysBetweenPurchases` | Numeric               | Average number of days between the customer's historical consecutive successful purchases.                      |

### Source

Derived from point-in-time successful purchase history and `Purchase Intervals`.

### Important Business Notes

For historical observations, the evaluation date is the applicable `ObservationDate`.

`DaysSinceLastPurchase` is calculated from the customer's most recent successful purchase known at the evaluation date.

`AverageDaysBetweenPurchases` is calculated from available purchase intervals rather than from the total age of the customer relationship.

---

## Dataset: Purchase Features

### Purpose

Stores customer-level evidence describing successful purchase volume, monetary behavior, and purchase frequency.

### Grain

One row per anonymous customer represented in the applicable successful purchase history.

| Field                  | Python Representation    | Description                                                                                                      |
| ---------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| `AnonymousCustomerKey` | String                   | Anonymous identifier of the customer represented by the feature record.                                          |
| `SuccessfulOrderCount` | Integer                  | Number of successful purchases represented in the applicable purchase history.                                   |
| `AverageOrderValue`    | Decimal-compatible value | Average `Total` across the customer's successful purchases, rounded to two decimal places using `ROUND_HALF_UP`. |
| `PurchaseFrequency`    | Numeric                  | Successful order count divided by the number of days between the customer's first and last successful purchases. |

### Source

Derived from point-in-time successful purchase history.

### Important Business Notes

`AverageOrderValue` uses NorthStar's currency rounding standard of two decimal places with `ROUND_HALF_UP`.

`PurchaseFrequency` measures successful purchases relative to the customer's active purchase span.

When the customer's first and last successful purchase occur on the same day, the active purchase span is zero and `PurchaseFrequency` remains missing rather than producing an infinite value.

---

## Dataset: Behavior Features

### Purpose

Stores customer-level evidence describing the consistency and directional change of historical purchase timing.

### Grain

One row per anonymous customer represented in `Purchase Intervals`.

| Field                    | Python Representation | Description                                                                    |
| ------------------------ | --------------------- | ------------------------------------------------------------------------------ |
| `AnonymousCustomerKey`   | String                | Anonymous identifier of the customer represented by the feature record.        |
| `PurchaseIntervalStdDev` | Numeric or missing    | Standard deviation of the customer's historical `DaysBetweenPurchases` values. |
| `AverageIntervalChange`  | Numeric or missing    | Average change between the customer's consecutive purchase intervals.          |

### Source

Derived from `Purchase Intervals` and `Purchase Interval Changes`.

### Reliable History Requirement

NorthStar v1.0 requires a minimum reliable history threshold of:

```text
MINIMUM_RELIABLE_HISTORY = 10
```

The threshold counts non-missing `DaysBetweenPurchases` values. Missing interval values do not contribute toward the minimum reliable history requirement.

Features requiring reliable purchase history remain missing when the applicable history does not satisfy this threshold.

### Important Business Notes

A lower `PurchaseIntervalStdDev` represents more consistent purchase timing, while a higher value represents greater timing variability.

A positive `AverageIntervalChange` indicates purchase intervals are becoming longer on average.

A negative value indicates purchase intervals are becoming shorter on average.

A missing value represents insufficient reliable evidence and is not equivalent to zero.

---

## Dataset: Customer Feature Dataset

### Purpose

Combines NorthStar's approved temporal, purchase, and behavior feature families into a reusable customer-level feature dataset.

### Grain

One row per anonymous customer represented in the assembled feature population.

| Field                         | Feature Family | Description                                                                                                                    |
| ----------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `AnonymousCustomerKey`        | Identifier     | Anonymous identifier used to preserve customer-level relationships without supplying customer identity as behavioral evidence. |
| `DaysSinceLastPurchase`       | Temporal       | Number of days since the customer's most recent successful purchase.                                                           |
| `AverageDaysBetweenPurchases` | Temporal       | Customer's average historical interval between successful purchases.                                                           |
| `SuccessfulOrderCount`        | Purchase       | Number of successful purchases in the applicable purchase history.                                                             |
| `AverageOrderValue`           | Purchase       | Average value of the customer's successful purchases.                                                                          |
| `PurchaseFrequency`           | Purchase       | Successful purchase count relative to the customer's active purchase span.                                                     |
| `PurchaseIntervalStdDev`      | Behavior       | Variability of the customer's historical purchase intervals.                                                                   |
| `AverageIntervalChange`       | Behavior       | Average directional change between consecutive purchase intervals.                                                             |

### Source

Assembled from:

* `Temporal Features`
* `Purchase Features`
* `Behavior Features`

using `AnonymousCustomerKey` as the customer-level relationship key.

### Important Business Notes

The Customer Feature Dataset contains reusable business evidence rather than model-specific inputs.

Historical versions of this dataset are generated using only successful purchase information available on or before the applicable observation date.

The customer population for a point-in-time feature dataset is determined from that same as-of successful purchase history, ensuring the feature population remains aligned with the applicable observation boundary.

Feature families are calculated independently and then assembled so that business logic remains separated, reusable, and maintainable.

# Business Interpretation

## Purpose

Business Interpretation converts reusable NorthStar business evidence into standardized business states and classifications.

For NorthStar Commerce v1.0, the Business Interpretation Engine defines the canonical interpretation of Customer Purchase Health.

Feature Engineering creates the evidence. Business Interpretation determines what that evidence means.

---

## Dataset: Purchase Health

### Purpose

Extends the assembled customer feature dataset with standardized Purchase Health measurements and a business-readable Purchase Health Tier.

### Grain

One row per anonymous customer represented in the input feature dataset.

| Field                         | Python Representation    | Description                                                                                                             |
| ----------------------------- | ------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| `AnonymousCustomerKey`        | String                   | Anonymous identifier of the customer represented by the Purchase Health record.                                         |
| `DaysSinceLastPurchase`       | Numeric                  | Number of whole days since the customer's most recent successful purchase.                                              |
| `AverageDaysBetweenPurchases` | Numeric                  | Average historical interval between the customer's successful purchases.                                                |
| `SuccessfulOrderCount`        | Integer                  | Number of successful purchases represented in the applicable purchase history.                                          |
| `AverageOrderValue`           | Decimal-compatible value | Average value of the customer's successful purchases.                                                                   |
| `PurchaseFrequency`           | Numeric                  | Successful purchase count relative to the customer's active purchase span.                                              |
| `PurchaseIntervalStdDev`      | Numeric or missing       | Variability of the customer's historical purchase intervals.                                                            |
| `AverageIntervalChange`       | Numeric or missing       | Average directional change between consecutive purchase intervals.                                                      |
| `HealthyWindowDays`           | Numeric or missing       | Upper boundary of the customer's expected healthy purchase window, calculated as 120% of `AverageDaysBetweenPurchases`. |
| `PercentBeyondHealthyWindow`  | Numeric or missing       | Relative amount by which `DaysSinceLastPurchase` exceeds `HealthyWindowDays`.                                           |
| `PurchaseHealthScore`         | Numeric or missing       | Standardized Purchase Health score from 0 to 100, where higher values represent healthier purchase behavior.            |
| `PurchaseHealthTier`          | String                   | Business-readable Purchase Health classification: `Healthy`, `Watch`, `At Risk`, `Critical`, or `Insufficient History`. |

### Source

Derived from the assembled Customer Feature Dataset by the Business Interpretation Engine.

### Healthy Window Calculation

```text
HealthyWindowDays =
    AverageDaysBetweenPurchases × 1.20
```

A valid Healthy Window requires a non-missing value greater than zero.

### Percent Beyond Healthy Window

When the customer remains within the Healthy Window:

```text
PercentBeyondHealthyWindow = 0
```

When the customer exceeds the Healthy Window:

```text
PercentBeyondHealthyWindow =
    (DaysSinceLastPurchase - HealthyWindowDays)
    / HealthyWindowDays
```

When valid historical evidence does not exist, the value remains missing.

### Purchase Health Score

When the customer remains within the Healthy Window:

```text
PurchaseHealthScore = 100
```

When the customer exceeds the Healthy Window:

```text
PurchaseHealthScore =
    100 - (PercentBeyondHealthyWindow × 100)
```

Scores below zero are floored at:

```text
PurchaseHealthScore = 0
```

When valid historical evidence does not exist, the score remains missing.

### Purchase Health Tier Thresholds

| Purchase Health Tier   | Purchase Health Score |
| ---------------------- | --------------------: |
| `Healthy`              |                95–100 |
| `Watch`                |                80–<95 |
| `At Risk`              |                60–<80 |
| `Critical`             |                 0–<60 |
| `Insufficient History` |     Score unavailable |

### Important Business Notes

`PurchaseHealthTier` defaults to `Insufficient History` until a valid `PurchaseHealthScore` exists.

Purchase Health is evaluated relative to the customer's own historical purchasing rhythm rather than against a universal inactivity threshold.

The Business Interpretation Engine provides the canonical Purchase Health interpretation used by downstream analytics and machine learning.

Machine learning consumes this business truth; it does not define the Purchase Health rules.

# Historical Machine Learning Dataset

## Purpose

The Historical Machine Learning Dataset stores point-in-time customer observations used to train NorthStar's predictive model.

Each record represents what NorthStar knew about an eligible customer at a specific `ObservationDate`, together with the customer's Purchase Health outcome 30 days later.

The dataset preserves the separation between observation-time evidence and future outcome information so that machine learning can learn from historical examples without future information leaking into the model inputs.

---

## Dataset: ML Training Dataset

### Purpose

Stores historical customer observations, Purchase Health interpretations, future Purchase Health outcomes, and the supervised machine learning target used for model development.

### Grain

One row per eligible anonymous customer per observation date.

### Observation Schedule

NorthStar v1.0 generates historical observations every:

```text
OBSERVATION_FREQUENCY_DAYS = 7
```

The prediction horizon is:

```text
PREDICTION_HORIZON_DAYS = 30
```

Observation dates are generated only when a complete 30-day future outcome period exists within the available historical data.

### Fields

| Field                           | Source                           | Description                                                                                                               |
| ------------------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `AnonymousCustomerKey`          | Feature Engineering              | Anonymous identifier of the customer represented by the historical observation.                                           |
| `DaysSinceLastPurchase`         | Feature Engineering              | Number of whole days since the customer's most recent successful purchase as of the observation date.                     |
| `AverageDaysBetweenPurchases`   | Feature Engineering              | Average historical interval between successful purchases known at the observation date.                                   |
| `SuccessfulOrderCount`          | Feature Engineering              | Number of successful purchases known at the observation date.                                                             |
| `AverageOrderValue`             | Feature Engineering              | Average value of successful purchases known at the observation date.                                                      |
| `PurchaseFrequency`             | Feature Engineering              | Successful purchase count relative to the customer's active purchase span as of the observation date.                     |
| `PurchaseIntervalStdDev`        | Feature Engineering              | Variability of historical purchase intervals when sufficient reliable history exists.                                     |
| `AverageIntervalChange`         | Feature Engineering              | Average directional change between consecutive purchase intervals when sufficient reliable history exists.                |
| `HealthyWindowDays`             | Business Interpretation          | Upper boundary of the customer's expected Healthy Window at the observation date.                                         |
| `PercentBeyondHealthyWindow`    | Business Interpretation          | Relative amount by which the customer's inactivity exceeds the Healthy Window at the observation date.                    |
| `PurchaseHealthScore`           | Business Interpretation          | Standardized Purchase Health score at the observation date.                                                               |
| `ObservationPurchaseHealthTier` | Business Interpretation          | Customer's Purchase Health Tier at the observation date.                                                                  |
| `OutcomePurchaseHealthTier`     | Future Business Interpretation   | Customer's Purchase Health Tier at the 30-day outcome date.                                                               |
| `AtRiskOrCriticalWithin30Days`  | Target Label                     | Binary supervised learning target indicating whether the customer is `At Risk` or `Critical` at the 30-day outcome point. |
| `ObservationDate`               | Historical Observation Generator | Point in time represented by the training record.                                                                         |

### Observation-Time Evidence

For each observation date, NorthStar reconstructs the feature dataset using only successful purchase information available at that point in time.

```text
Business History
        ↓
Observation Date
        ↓
Point-in-Time Feature Dataset
        ↓
Business Interpretation
        ↓
Observation Purchase Health
```

Future purchases do not contribute to observation-time feature values.

### Outcome Date

The future outcome date is calculated as:

```text
OutcomeDate =
    ObservationDate + 30 days
```

NorthStar generates a second interpreted Purchase Health snapshot at the outcome date and compares it with the customer's observation-time record.

### Eligible Observation Population

Historical observations are retained for supervised learning when:

```text
ObservationPurchaseHealthTier
    ∈ {Healthy, Watch, At Risk}
```

Observations where the customer is already `Critical` are excluded from the prediction population.

### Target Label

The supervised machine learning target is:

```text
AtRiskOrCriticalWithin30Days
```

Target values are assigned as follows:

```text
OutcomePurchaseHealthTier
        ↓
At Risk or Critical?
    ├── Yes → AtRiskOrCriticalWithin30Days = 1
    └── No  → AtRiskOrCriticalWithin30Days = 0
```

A value of `1` therefore means that the customer is `At Risk` or `Critical` at the future outcome date.

A value of `0` means that the customer is not `At Risk` or `Critical` at that point.

### Important Business Notes

The target does not measure whether the customer's Purchase Health Tier changed.

For example, a customer who is `At Risk` on the observation date and remains `At Risk` 30 days later receives a target value of `1`.

`ObservationPurchaseHealthTier` and `OutcomePurchaseHealthTier` are preserved to establish historical business truth and traceability.

Future outcome information is used only to construct the supervised target and must not be supplied to the model as observation-time evidence.

Multiple historical observations may exist for the same `AnonymousCustomerKey` because each row represents the customer's state at a different point in time.

# Machine Learning Development Datasets

## Purpose

NorthStar separates historical machine learning observations chronologically so model development reflects the real prediction problem: learning from earlier customer behavior and evaluating predictions against later customer outcomes.

The historical ML dataset is divided into five temporally separated populations:

1. Training
2. Validation Embargo
3. Validation
4. Final Test Embargo
5. Final Test

Embargo periods prevent observations near temporal boundaries from participating in model development or final evaluation.

---

## Dataset: Training Data

### Purpose

Provides the historical observations used to train the NorthStar baseline machine learning model.

### Grain

One row per eligible anonymous customer per historical observation date.

### Temporal Boundary

```text
ObservationDate <= 2025-09-01
```

### Important Business Notes

Only the explicitly approved model features are supplied to the model.

Customer identifiers, observation dates, Purchase Health tiers, and future outcome information are excluded from model features.

---

## Dataset: Validation Embargo

### Purpose

Provides temporal separation between the Training and Validation populations.

### Temporal Boundary

```text
2025-09-01 < ObservationDate < 2025-10-01
```

### Important Business Notes

Records within this period are excluded from model training and validation-based model-development decisions.

The embargo helps preserve chronological separation around the validation boundary.

---

## Dataset: Validation Data

### Purpose

Provides a temporally later population for model-development decisions before final testing.

NorthStar v1.0 uses the validation population to evaluate decision-threshold tradeoffs and select the model's operational classification threshold.

### Temporal Boundary

```text
2025-10-01 <= ObservationDate < 2025-12-01
```

### Important Business Notes

Validation data may inform model-development decisions.

It is separate from the Final Test population so those decisions can be locked before final evaluation.

---

## Dataset: Final Test Embargo

### Purpose

Provides temporal separation between model-development observations and the Final Test population.

### Temporal Boundary

```text
2025-12-01 < ObservationDate < 2026-01-01
```

### Important Business Notes

Records within this period are excluded from both model development and final model evaluation.

The embargo preserves additional temporal separation before the unseen Final Test population.

---

## Dataset: Final Test Data

### Purpose

Provides the chronologically later, unseen population used to evaluate NorthStar's completed v1.0 model after model-development decisions have been locked.

### Grain

One row per eligible anonymous customer per historical observation date.

### Temporal Boundary

```text
ObservationDate >= 2026-01-01
```

### Important Business Notes

Final Test data must not be used to select the decision threshold or make other model-development decisions.

The Final Test population judges the completed model against later customer behavior.

---

## Approved Model Inputs

NorthStar v1.0 explicitly approves the following fields as machine learning evidence:

| Field                         | Description                                                                |
| ----------------------------- | -------------------------------------------------------------------------- |
| `DaysSinceLastPurchase`       | Customer purchase recency at the observation date.                         |
| `AverageDaysBetweenPurchases` | Customer's historical average purchase interval.                           |
| `SuccessfulOrderCount`        | Number of successful purchases known at the observation date.              |
| `AverageOrderValue`           | Average value of the customer's successful purchases.                      |
| `PurchaseFrequency`           | Successful purchase count relative to the customer's active purchase span. |
| `PurchaseIntervalStdDev`      | Variability of the customer's historical purchase timing.                  |
| `AverageIntervalChange`       | Average directional change in the customer's purchase intervals.           |
| `HealthyWindowDays`           | Upper boundary of the customer's expected purchase window.                 |
| `PercentBeyondHealthyWindow`  | Relative amount by which customer inactivity exceeds the Healthy Window.   |
| `PurchaseHealthScore`         | Standardized observation-time Purchase Health score.                       |

### Approved Missing Feature Values

NorthStar permits missing values for:

```text
PurchaseIntervalStdDev
AverageIntervalChange
```

These missing values represent insufficient reliable purchase history rather than zero-valued customer behavior.

---

## Model Target

The supervised machine learning target is:

```text
AtRiskOrCriticalWithin30Days
```

The target is separated from the approved model features before model training.

---

## Traceability Fields

`AnonymousCustomerKey` and `ObservationDate` remain associated with historical observations for traceability but are not supplied to the model as predictive evidence.

---

## Decision Threshold

NorthStar v1.0 uses:

```text
MODEL_DECISION_THRESHOLD = 0.325
```

Predicted probabilities are converted into operational classifications according to:

```text
AtRiskOrCriticalProbability >= 0.325
    ├── True  → PredictedAtRiskOrCritical = True
    └── False → PredictedAtRiskOrCritical = False
```

The threshold is selected using temporally protected validation data and locked before Final Test evaluation.

### Important Business Notes

NorthStar prioritizes positive-class recall because false negatives carry greater business cost than false positives for the Customer Purchase Health prediction problem.

The threshold balances identifying customers who become `At Risk` or `Critical` against the operational workload created by false-positive predictions.

Accuracy alone is not used to determine the appropriate operating threshold.

# Prediction Outputs

## Purpose

Prediction Outputs store the results produced by the NorthStar v1.0 machine learning model for the Final Test population.

The output preserves customer-level traceability while separating model predictions from the historical training and evaluation datasets.

---

## Dataset: Customer Purchase Health Predictions

### Purpose

Stores the model's predicted probability that a customer will be `At Risk` or `Critical` within 30 days, together with the classification produced using NorthStar's approved decision threshold.

### Grain

One row per anonymous customer per Final Test observation date.

| Field                         | Python Representation | Description                                                                                                                           |
| ----------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `AnonymousCustomerKey`        | String                | Anonymous customer identifier retained for traceability and downstream use.                                                           |
| `ObservationDate`             | Date-compatible value | Historical observation date associated with the prediction.                                                                           |
| `AtRiskOrCriticalProbability` | Numeric               | Model-estimated probability that the customer will be `At Risk` or `Critical` 30 days from the observation date.                      |
| `PredictedAtRiskOrCritical`   | Boolean               | Threshold-based classification indicating whether the predicted probability meets or exceeds NorthStar's approved decision threshold. |

### Source

Generated by the Machine Learning Engine from predictions produced against the Final Test feature population.

### Probability Output

`AtRiskOrCriticalProbability` is generated from the model's positive-class probability:

```text
predict_proba(X_test)[:, 1]
```

The value represents the model's estimated probability of:

```text
AtRiskOrCriticalWithin30Days = 1
```

### Classification Output

NorthStar converts the predicted probability into a business-facing classification using:

```text
MODEL_DECISION_THRESHOLD = 0.325
```

Classification logic:

```text
AtRiskOrCriticalProbability >= 0.325
    ├── True  → PredictedAtRiskOrCritical = True
    └── False → PredictedAtRiskOrCritical = False
```

### Important Business Notes

`AnonymousCustomerKey` is retained for traceability but is not supplied to the model as a predictive feature.

`ObservationDate` identifies the point in time represented by the prediction and is also excluded from the model feature set.

`AtRiskOrCriticalProbability` preserves the model's continuous risk estimate before the decision threshold is applied.

`PredictedAtRiskOrCritical` represents the operational classification produced from that probability.

The prediction output identifies elevated future Purchase Health risk. It does not prescribe a business action.

NorthStar's model determines **who may be at risk**; the business determines **what action, if any, should follow**.
