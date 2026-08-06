# NorthStar Commerce
## Data Dictionary

Version 1.0

---

# Overview

This document describes the structure, purpose, and business meaning of every table and column within the NorthStar Commerce SQL Server database.

The NorthStar Commerce database was designed as a realistic synthetic e-commerce environment for learning SQL, database design, analytics, Power BI, Python, and data engineering.

---

# Table: Categories

## Purpose

Stores the product categories available throughout NorthStar Commerce.

| Column       | Data Type    | Description                                             |
| ------------ | ------------ | ------------------------------------------------------- |
| CategoryID   | TINYINT      | Unique identifier for each product category.            |
| CategoryName | NVARCHAR(50) | Human-readable category name used to classify products. |

---

# Table: Customers

## Purpose

Stores demographic information, account attributes, and behavioral characteristics for every customer in NorthStar Commerce. This table represents the master customer record used throughout the enterprise.

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

Primary Key

CustomerID

Referenced By

Orders.CustomerID