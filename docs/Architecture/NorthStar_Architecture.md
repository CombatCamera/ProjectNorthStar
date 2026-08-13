# NorthStar Architecture

## 1. Purpose
Project NorthStar is a modular enterprise analytics and machine learning platform designed to simulate realistic business operations, generate behavioral datasets, protect customer privacy, and enable predictive analytics through reusable learning pipelines.

## 2. Engineering Laws:

### Law #1 – Every Field Must Earn Its Place.
Data exists to answer questions, not to fill tables.

### Law #2 – Every Engine Has One Responsibility.
Each engine should have a single, clearly defined responsibility.
If an engine begins solving multiple unrelated problems, the architecture should be reconsidered.

### Law #3 – No Useful Idea Is Discarded.
Ideas that do not belong to the current engine are intentionally parked for the future engine that owns that responsibility.


## 3. Decision Process

            Business Question
                    ↓
            Architecture Discussion
                    ↓
            Field Evaluation
                    ↓
            Engine Ownership
                    ↓
            Implementation
                    ↓
            QA


## 3. Core Design Principles
One component, one responsibility.
Behavior over identity.
Privacy by design.
Learn from evidence, not labels.
Synthetic training, real-world applicability.
Architecture before implementation.
Modularity over monolithic design.

## 4. Design Philosophy
NorthStar is built as a collection of independent, single-responsibility engines connected through well-defined data pipelines. Each engine should solve one problem well while remaining reusable by future systems.

## 5. Emergent Architecture
NorthStar is not designed by attempting to define every engine in advance. Instead, engines emerge naturally as business questions reveal distinct responsibilities. New engines are created only when they solve a clearly defined problem that cannot be cleanly owned by an existing engine.

The architecture evolves through disciplined questioning rather than speculation. Every component, engine, and data field must earn its place by solving a specific problem or answering a specific business question.


Example:

            Question:
            "Could shipping costs influence customer behavior?"

            ↓

            Discovery:
            Shipping belongs to a Context Engine.

            ↓

            Question:
            "Who explains why customer behavior changed?"

            ↓

            Discovery:
            Behavior Influence Engine.

            ↓

            Architecture evolves.


## 6. High-Level System Architecture

            NorthStar Commerce
                    │
                    ▼
            Privacy Engine
                    │
                    ▼
            Purchase Health Engine
                    │
                    ▼
            Training Dataset Generator
                    │
                    ▼
            Machine Learning Engine
                    │
                    ▼
            Prediction Engine

## 7. Major Components

Every component follows the same template:

- Purpose
- Inputs
- Outputs
- Responsibilities
- Non-Responsibilities

---

### Privacy Engine

**Purpose**

Protect customer privacy while preserving business 
relationships across datasets.

**Inputs**

- Customers
- Orders
- Payments

**Outputs**

- Anonymous Customers
- Anonymous Orders
- Anonymous Payments

**Responsibilities**

- Generate dataset-scoped anonymous customer mapping.
- Replace CustomerID with AnonymousCustomerKey.
- Remove unnecessary identifying information.
- Preserve relationships across tables.

**Non-Responsibilities**

- Feature engineering
- Machine learning
- Prediction
- Analytics

---

### Purchase Health Engine

Purpose *(To be completed)*

Inputs *(To be completed)*

Outputs *(To be completed)*

Responsibilities *(To be completed)*

Non-Responsibilities *(To be completed)*

---

### Training Dataset Generator

...

Purpose *(To be completed)*

Inputs *(To be completed)*

Outputs *(To be completed)*

Responsibilities *(To be completed)*

Non-Responsibilities *(To be completed)*

---


## 8. Data Flow
            NorthStar Commerce
                    ↓
            Privacy Engine
                    ↓
            Purchase Health Engine
                    ↓
            Training Dataset Generator
                    ↓
            Machine Learning Engine
                    ↓
            Prediction Engine

## 9. Future Engines
Customer Service Engine
Fraud Detection Engine
Inventory Forecasting Engine
Supply Chain Engine
NorthStar Live
Project Inspire integration

## 10. Future Feature Candidates

| Field          |  Status | Future Engine             | Reason                                                                            |
| -------------- | ------- | ------------------------- | --------------------------------------------------------------------------------- |
| DiscountRate   | 🅿️ Park | Customer Retention Engine | Business intervention that may influence future purchases.                        |
| DiscountAmount | 🅿️ Park | Customer Retention Engine | Same reason.                                                                      |
| ShippingMethod | 🅿️ Park | Logistics Engine          | May help study customer shipping preferences and shipping strategy effectiveness. |
| Shipping       | 🅿️ Park | Context Engine            | External business condition that may influence customer behavior.                 |
| Tax            | 🅿️ Park | Context Engine            | Tax policy, tariffs, and other external economic influences.                      |
| Total          | 🅿️ Park | Revenue Analytics Engine  | Financial analytics rather than Purchase Health.                                  |
| PaymentID      | 🅿️ Park | Payment Analytics Engine  | Transaction-level analytics, refunds, and payment operations.                     |

## 11. Feature Selection Philosophy

Every field must earn its place.

When evaluating a field:

1. Does it directly help answer the current business question? → Keep
   
2. Is it valuable for a different engine? → Park
   
3. Does it provide no meaningful value? → Exclude
   
4. Can it be calculated later from other data? → Derive