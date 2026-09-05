# NorthStar Commerce Architecture

## System Purpose

NorthStar Commerce is a synthetic enterprise analytics platform designed to generate realistic business data, validate that data against defined business rules, protect privacy, engineer reusable business evidence, interpret customer purchase health, generate point-in-time machine learning training data, and produce predictive customer-risk outputs.

The architecture is designed so that each layer has a clear responsibility and
passes certified data forward to the next layer.

## High-Level Architecture

NorthStar Commerce is organized as a sequence of specialized layers. Each layer
has one primary responsibility and passes its output forward only after the
required business rules and quality checks have been satisfied.
```text
Generation Engine
    ↓
QA Certification
    ↓
Privacy Engine
    ↓
Business Data Preparation
    ↓
Feature Engineering
    ↓
Business Interpretation
    ↓
ML Training Dataset Generation
    ↓
Machine Learning Engine
    ↓
Prediction Output
```
This layered design keeps data generation, validation, privacy protection,
business logic, feature creation, interpretation, and machine learning
separate from one another.

## Generation Layer

The NorthStar Commerce Generation Engine creates the synthetic enterprise
environment that serves as the foundation for the rest of the system.

The Generation Engine is the single source of truth for synthetic business
data generation. Business rules governing customers, products, purchasing
behavior, orders, financial calculations, payments, and shipments are defined
once and reused when generating different NorthStar populations.

### Generated Datasets

- `customers.csv`
- `categories.csv`
- `products.csv`
- `orders.csv`
- `order_items.csv`
- `payments.csv`
- `shipments.csv`

### Population Architecture

NorthStar currently supports two independently generated populations:

| Population             | Purpose                                                                                                          |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Operational Population | Represents the primary NorthStar Commerce enterprise dataset used for analytics and business analysis.           |
| Training Population    | Provides an independent synthetic population for historical feature generation and machine learning development. |

Both populations use the same Generation Engine and business rules while
remaining separate datasets.

This allows NorthStar to create independent business populations without
duplicating generation logic.



## QA Certification Layer

The NorthStar Commerce QA Engine validates generated enterprise datasets before
they are approved for downstream processing.

QA operates independently from data generation. The Generation Engine creates
the business environment; the QA Engine determines whether that environment
satisfies NorthStar's defined business and structural rules.

### Core Validation Areas

- Referential integrity
- Financial integrity
- Timeline consistency
- Business-rule compliance
- Shipment lifecycle validation when applicable
- Dataset certification

### Certification Flow

```text
Generated Dataset
       ↓
QA Validation
       ↓
All Applicable Checks Pass?
       ├── No  → Dataset Fails Certification
       └── Yes → Dataset Certified
                         ↓
                 Downstream Processing
```

NorthStar uses a fail-closed approach to certification. A dataset that fails an
applicable QA rule is not considered approved for downstream use.

The QA Engine can validate both operational and training populations while
applying only the checks relevant to the datasets that exist.

## Privacy Layer

The NorthStar Privacy Engine transforms QA-certified enterprise data into
privacy-preserving analytical data while retaining the business relationships
required for downstream analysis.

Privacy protection is performed after source-data certification and before
privacy-preserved data is supplied to downstream analytical processes.

### Current Privacy Transformations

- Customer anonymization using dataset-scoped UUID mappings
- Order anonymization using UUID mappings
- Personally identifiable information (PII) removal through field whitelists
- Customer-scoped temporal offsets
- Relationship reconstruction across retained datasets
- Configurable dataset selection

### Privacy Data Flow

```text
QA-Certified Enterprise Data
             ↓
      Privacy Engine
             ↓
   Remove Unapproved Fields
             ↓
   Anonymize Identifiers
             ↓
 Apply Temporal Protection
             ↓
 Preserve Required Relationships
             ↓
Privacy-Preserved Analytical Data
```

Customer-scoped temporal offsets preserve the relative timing of a customer's
business events while protecting the original event timeline.

### Privacy Boundary

The Privacy Engine transforms data but does not determine business meaning,
generate features, train machine learning models, or perform source-data
certification.

Privacy-output QA certification remains a future enhancement. The current
NorthStar Commerce QA Engine certifies source datasets before they enter the
Privacy Engine.

## Business Data Preparation

Business Data Preparation converts privacy-preserved business events into
reusable business data objects that can support multiple downstream features.

This layer exists to prevent Feature Engineering from repeatedly reconstructing
the same business relationships. Business events are organized once and then
reused as the foundation for feature calculations.

### Current Business Data Objects

| Business Data Object                    | Purpose                                                                         |
| --------------------------------------- | ------------------------------------------------------------------------------- |
| Successful Purchase History             | Establishes the customer's history of successful purchases.                     |
| Purchase History As Of Observation Date | Restricts purchase history to information available at a defined point in time. |
| Purchase Intervals                      | Measures the number of days between successful purchases.                       |
| Purchase Interval Changes               | Measures how purchase intervals change from one interval to the next.           |

### Data Preparation Flow

```text
Privacy-Preserved Business Events
               ↓
    Successful Purchase History
               ↓
 Purchase History As Of Observation Date
               ↓
       Purchase Intervals
               ↓
   Purchase Interval Changes
               ↓
      Reusable Business Objects
               ↓
        Feature Engineering
```

For historical observations, Business Data Preparation applies the point-in-time
boundary:

`OrderDateTime` <= `ObservationDate`

Events occurring after the observation date are excluded from the business
objects used to generate that historical observation.

### Architectural Principle

Business Data Preparation organizes business events into reusable knowledge.
Feature Engineering uses that knowledge to answer specific business questions.

## Feature Engineering Layer

Feature Engineering transforms reusable business data objects into measurable
business evidence.

Each feature exists to answer a defined business question. Feature Engineering
does not decide what the evidence means and does not make predictions. Its
responsibility is to calculate the evidence accurately and consistently.

### Feature Design Flow

```text
        Business Question
                ↓
         Feature (Answer)
                ↓
          Business Rules
                ↓
             Function
                ↓
                QA
```

| Feature Family    | Current Evidence                                                 |
| ----------------- | ---------------------------------------------------------------- |
| Temporal Features | `DaysSinceLastPurchase`, `AverageDaysBetweenPurchases`           |
| Purchase Features | `SuccessfulOrderCount`, `AverageOrderValue`, `PurchaseFrequency` |
| Behavior Features | `PurchaseIntervalStdDev`, `AverageIntervalChange`                |
| Payment Features  | Future                                                           |

### Historical Feature Generation

Feature Engineering supports both current-state and historical point-in-time
feature generation.

For a historical observation, only business information available on or before
the `ObservationDate` may contribute to the generated features. This ensures
that future information cannot enter the evidence later supplied to machine
learning.

### Feature Engineering Principle
> **Every feature is the answer to a business question.**


Evidence is generated once and passed forward through the architecture rather
than being independently recalculated by downstream systems.

## Business Interpretation Layer

Business Interpretation converts engineered evidence into defined business
meaning.

Feature Engineering answers measurable business questions. Business
Interpretation applies NorthStar's defined business rules to that evidence to
determine the customer's current purchase-health state.

### Current Purchase Health Interpretation

The Customer Purchase Health Engine uses engineered evidence to calculate:

- `HealthyWindowDays`
- `PercentBeyondHealthyWindow`
- `PurchaseHealthScore`
- Purchase Health Tier

Current purchase-health tiers are:

- Healthy
- At Risk
- Critical
- Insufficient History

### Interpretation Flow

```text
Engineered Business Evidence
             ↓
     Business Rules
             ↓
      Healthy Window
             ↓
Percent Beyond Healthy Window
             ↓
   Purchase Health Score
             ↓
    Purchase Health Tier
             ↓
     Business Meaning
```

### Separation from Machine Learning

Business Interpretation defines the outcome that NorthStar considers meaningful.
Machine learning does not define customer purchase health.

This separation allows NorthStar to establish business truth independently and
then train a model to anticipate that truth at a future point in time.

### Business Interpretation Principle
> **One engine creates the business truth. The second engine learns to anticipate it.**

## ML Training Dataset Generation

The ML Training Dataset Generator reconstructs historical customer states and
creates point-in-time supervised learning examples.

Each training record represents what NorthStar could have known about a
customer on a specific `ObservationDate`, paired with the business outcome
observed after the defined prediction horizon.

### Prediction Question

> **Will this customer be At Risk or Critical 30 days from the observation date?**

The supervised learning target is:

`AtRiskOrCriticalWithin30Days`

### Historical Training Flow

```text
        Historical Business Data
                ↓
        Observation Date
                ↓
        Point-in-Time Features
                ↓
        Business Interpretation
                ↓
        Observation Purchase Health
                ↓
        30-Day Prediction Horizon
                ↓
        Outcome Purchase Health
                ↓
        Target Label
                ↓
        ML Training Record
```

### Point-in-Time Rule

Features for a historical training observation may use only information that
was available on or before its `ObservationDate`.

Future information may be used to determine the customer's outcome and target
label, but it may not contribute to the features presented to the model.

### Training Record Structure

Each training observation contains:

- Anonymous customer identifier
- Observation date
- Point-in-time engineered features
- Observation purchase-health interpretation
- Future purchase-health outcome
- Supervised learning target

This structure allows NorthStar to teach the model using historical examples
without allowing future information to leak into the evidence used for
prediction.

## Temporal Training Architecture

NorthStar separates historical observations by time so that model development
and final evaluation represent realistic prediction against future data.

The temporal architecture includes two embargo periods that create separation
between training, validation, and final testing.

### Temporal Split

```text
               Training
        2023-01-01 → 2025-08-31
                   ↓
           Validation Embargo
        2025-09-01 → 2025-09-30
                   ↓
              Validation
        2025-10-01 → 2025-11-30
                   ↓
          Final Test Embargo
        2025-12-01 → 2025-12-31
                   ↓
              Final Test
          2026-01-01 → Future
```

### Dataset Responsibilities
|Dataset|Purpose|
|---|---|
|Training|Used to teach the model historical relationships between customer evidence and future outcomes. |
|Validation Embargo|	Creates temporal separation between training and validation observations.|
|Validation|	Used for model-development decisions, including selection of the decision threshold.|
|Final Test Embargo|	Creates temporal separation between validation and the final unseen test period.|
|Final Test|	Used only after model-development decisions are locked to evaluate performance against unseen future observations.|

### Validation Boundary

Model-development decisions are made using the validation period without using
the final test period to select those decisions.

For NorthStar v1.0, the decision threshold was selected using validation data
and then locked before final test evaluation.

### Temporal Integrity Principle

> **Biff cannot see information from the future before Biff is allowed to learn.**

## Machine Learning Engine

The Machine Learning Engine learns relationships between historical customer
evidence and future purchase-health outcomes.

NorthStar v1.0 uses a `HistGradientBoostingClassifier` to estimate the
probability that a customer will be At Risk or Critical within the 30-day
prediction horizon.

### Model Feature Contract

The v1.0 model receives ten approved features:

| Feature                       | Evidence Represented                                          |
| ----------------------------- | ------------------------------------------------------------- |
| `DaysSinceLastPurchase`       | Customer purchase recency                                     |
| `AverageDaysBetweenPurchases` | Typical purchase interval                                     |
| `SuccessfulOrderCount`        | Successful purchase history                                   |
| `AverageOrderValue`           | Typical successful order value                                |
| `PurchaseFrequency`           | Historical purchase frequency                                 |
| `PurchaseIntervalStdDev`      | Variability in purchase timing                                |
| `AverageIntervalChange`       | Direction and magnitude of purchase-interval change           |
| `HealthyWindowDays`           | Customer-specific expected purchase window                    |
| `PercentBeyondHealthyWindow`  | Degree to which current inactivity exceeds the healthy window |
| `PurchaseHealthScore`         | Current interpreted purchase-health score                     |

### Excluded Model Inputs

The training dataset contains additional fields that are intentionally excluded
from model features.

| Field                           | Reason for Exclusion                                                                  |
| ------------------------------- | ------------------------------------------------------------------------------------- |
| `AnonymousCustomerKey`          | Retained for traceability, not customer behavior.                                     |
| `ObservationDate`               | Used for temporal control and traceability, not supplied as a raw v1.0 model feature. |
| `ObservationPurchaseHealthTier` | Retained for interpretation and diagnostics rather than model input.                  |
| `OutcomePurchaseHealthTier`     | Future outcome information; supplying it to the model would cause target leakage.     |
| `AtRiskOrCriticalWithin30Days`  | Prediction target (`y`), not an input feature (`X`).                                  |

### Missing Evidence

`PurchaseIntervalStdDev` and `AverageIntervalChange` may contain missing values
when a customer does not yet have enough reliable purchase history to calculate
the behavior feature.

NorthStar preserves this missing state rather than replacing it with zero,
because zero represents real behavioral evidence and is not equivalent to
insufficient evidence.

The selected model can natively process these missing feature values.

### Machine Learning Flow

```text
    Approved Historical Features (X)
                +
        Training Target (y)
                ↓
            Train Model
                ↓
    Customer Feature Evidence
                ↓
    Predicted Risk Probability
                ↓
        Decision Threshold
                ↓
        Predicted Risk Flag
```

## Decision Threshold Architecture

The Machine Learning Engine produces a probability representing the estimated
risk that a customer will be At Risk or Critical within the 30-day prediction
horizon.

NorthStar converts that probability into an operational prediction using a
defined decision threshold.

### NorthStar v1.0 Threshold

`MODEL_DECISION_THRESHOLD = 0.325`

```text
Predicted Probability
         ↓
Probability >= 0.325?
    ├── No  → PredictedAtRiskOrCritical = False
    └── Yes → PredictedAtRiskOrCritical = True
``` 
The threshold was selected using the temporally protected validation dataset.
The final test dataset was not used to select or adjust the threshold.

### Business Priority

NorthStar treats a false negative as the more costly prediction error because
it represents a customer who becomes At Risk or Critical without being flagged
by the model.

However, lowering the threshold also increases false positives and therefore
the number of customers who may require unnecessary review or intervention.

The selected threshold balances two operational goals:

- Identify a useful proportion of customers who will become At Risk or Critical.
- Keep false-positive alert volume at a reasonable operational level.
  
### Threshold Selection Principle

> **The decision threshold is a business decision informed by model performance, not simply a mathematical default.**

## Prediction Output Layer

The Machine Learning Engine converts final model predictions into a persistent
historical prediction artifact that can be consumed by downstream analytical
systems.

The prediction output preserves customer and observation traceability while
keeping those identifiers separate from the features used by the model.

### Prediction Output Contract

The historical prediction artifact contains:

| Field                         | Purpose                                                                                                |
| ----------------------------- | ------------------------------------------------------------------------------------------------------ |
| `AnonymousCustomerKey`        | Identifies the anonymous customer associated with the prediction.                                      |
| `ObservationDate`             | Identifies the historical point in time represented by the prediction.                                 |
| `AtRiskOrCriticalProbability` | Stores the model's estimated probability that the customer will be At Risk or Critical within 30 days. |
| `PredictedAtRiskOrCritical`   | Stores the operational prediction produced by applying the decision threshold.                         |

### Output Artifact

`customer_purchase_health_predictions.csv`

### Prediction Output Flow

```text
    Final Test Customer Evidence
                ↓
        Trained Model
                ↓
        Risk Probability
                ↓
        Decision Threshold
                ↓
        Prediction Flag
                ↓
    Assemble Prediction Output
                ↓
            Save Artifact
```
### Output QA

The Machine Learning Engine QA validates the saved prediction artifact before
it is considered certified.

Current output validations confirm:

- Exact output schema
- Correct output row count
- Customer and observation-date population alignment
- Probability values remain within the valid 0–1 range
- Prediction values are valid binary outcomes
- Required output values are not missing

Observation alignment is based on the customer and observation-date population,
not the physical row order of the saved file.

### Architectural Boundary

The historical prediction artifact records what the trained model predicted.
It does not perform operational customer intervention or retention activity.

Future operational systems may consume model predictions and associate them
with real customer identities, workflows, dashboards, alerts, or other
authorized business processes.

## Architectural Boundaries

NorthStar Commerce separates responsibilities so that each layer performs a
defined job without absorbing the responsibilities of neighboring layers.

| Layer                          | Primary Responsibility                                                | Does Not Decide                         |
| ------------------------------ | --------------------------------------------------------------------- | --------------------------------------- |
| Generation                     | Create the synthetic business environment                             | Whether generated data passes QA        |
| QA Certification               | Validate generated business data                                      | How data is generated                   |
| Privacy                        | Protect sensitive information while preserving required relationships | Business meaning or predictions         |
| Business Data Preparation      | Organize business events into reusable business objects               | What those events mean                  |
| Feature Engineering            | Generate measurable business evidence                                 | Customer purchase-health classification |
| Business Interpretation        | Convert evidence into defined business meaning                        | Future model predictions                |
| ML Training Dataset Generation | Construct point-in-time supervised learning examples                  | Model behavior                          |
| Machine Learning               | Learn from historical evidence and estimate future risk               | Definition of business truth            |
| Prediction Output              | Preserve predictions in a reusable artifact                           | Operational customer intervention       |

Information moves forward through these boundaries rather than allowing
downstream systems to independently recreate upstream business logic.

## Core Architectural Principles

NorthStar Commerce follows several principles across the system:

- Prefer the simplest design that remains clear, maintainable, and teachable.
- Every feature is the answer to a business question.
- Shared business rules should have one source of truth.
- Generate data once and reuse it many times.
- Business truth is defined independently of machine learning.
- Historical evidence may contain only information available at the observation
  date.
- Future information may define a supervised-learning outcome but must never
  leak into observation-time model evidence.
- QA remains separate from the production logic it validates.
- Failed certification must block output where fail-closed behavior is required.
- Missing evidence must not silently become valid evidence.
- Knowledge should flow forward through the architecture rather than being
  repeatedly reconstructed downstream.

### Responsibility Principle

> **Orchestration coordinates; specialist modules perform the work.**

## Purchase Health Eligibility

The Customer Purchase Health Engine requires observable purchase behavior
before customer purchase health can be evaluated.

### Input Population

Customers must have at least one successful purchase before entering the
Purchase Health population.

### Eligibility Rule

```text
Customer
    ↓
At Least One Successful Purchase?
    ├── No  → Not Eligible for Purchase Health Evaluation
    └── Yes → Eligible for Purchase Health Evaluation
```
### Business Reason

Purchase behavior cannot be measured before a successful purchase exists.

Customers without a successful purchase therefore remain outside the Purchase
Health population rather than being assigned a purchase-health classification.

## Execution and Orchestration Architecture

NorthStar Commerce uses orchestration code to coordinate the execution of
specialist modules without duplicating the business logic owned by those
modules.

Orchestration determines when work occurs and how outputs move through the
pipeline. Specialist modules remain responsible for performing the work.

### Execution Relationship

```text
        Orchestration
             ↓
    Coordinate Execution
             ↓
     Specialist Modules
             ↓
       Perform Work
             ↓
      Return Results
             ↓
    Continue Pipeline
```

This separation keeps business rules, feature calculations, validation logic,
and machine learning behavior inside the modules that own those responsibilities.

Orchestration therefore coordinates the system rather than becoming another
location where business logic must be maintained.

## NorthStar Commerce v1.0 Boundary

NorthStar Commerce v1.0 ends with the generation and certification of the
historical machine learning prediction artifact.

```text
Historical Business Environment
             ↓
   Certified Business Data
             ↓
   Privacy-Preserved Data
             ↓
      Business Evidence
             ↓
       Business Truth
             ↓
 Historical ML Training Data
             ↓
       Trained Model
             ↓
    Historical Predictions
             ↓
     Certified Artifact
        ← v1.0 Boundary →
```

Operational deployment is intentionally outside the v1.0 architecture.

Future NorthStar architecture may extend beyond this boundary to support model
persistence and loading, current-state scoring, operational customer workflows,
dashboards, alerts, and the continuously operating NorthStar Live environment.

These future capabilities should extend the certified v1.0 architecture rather
than redefine the business rules and responsibilities already established
within it.