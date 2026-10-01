# Project NorthStar

## Customer Purchase Health & Predictive Retention Analytics

Project NorthStar is an end-to-end data analytics and machine learning project
built around a realistic synthetic e-commerce environment.

The project follows customer behavior from raw transactional data through data
generation, quality assurance, privacy protection, feature engineering,
business interpretation, historical machine learning dataset generation, and
predictive modeling.

Its central business question is:

> **Which customers are showing signs of deteriorating purchase health, and which
> customers are likely to become At Risk or Critical within the next 30 days?**

NorthStar was designed not simply to produce a prediction, but to demonstrate
the complete engineering and analytical process required to create one that is
traceable, testable, privacy-conscious, and useful for business decision-making.

## Project Overview

NorthStar models an e-commerce business environment and follows customer
purchase behavior through a complete analytical pipeline.

The project begins with the generation of realistic synthetic business data.
That data is validated before moving through privacy protection, feature
engineering, and business interpretation.

Customer purchase behavior is evaluated using metrics such as purchase timing,
purchase frequency, purchase consistency, and deviation from each customer's
historical purchasing pattern.

These signals are used to classify customer purchase health into five business
tiers:

- **Healthy**
- **Watch**
- **At Risk**
- **Critical**
- **Insufficient History**

NorthStar then creates point-in-time historical observations and uses future
customer outcomes to train a machine learning model that predicts whether an
eligible customer will be **At Risk or Critical within the next 30 days**.

The final prediction provides a probability of future purchase-health
deterioration while leaving the business decision—such as whether and how to
contact the customer—to the appropriate business team.

## End-to-End Pipeline

NorthStar is organized as a sequence of independent but connected stages. Each
stage has a defined responsibility and produces data for the next stage.

<div align="center">
<pre>
Synthetic Business Data Generation
↓
Data Quality Assurance
↓
Privacy Protection
↓
Business Data Preparation
↓
Feature Engineering
↓
Business Interpretation
↓
Historical Observation Generation
↓
Target Label Generation
↓
Temporal Machine Learning Split
↓
Model Training and Validation
↓
Threshold Selection
↓
Final Test Evaluation
↓
Customer Risk Predictions
</pre>
</div>

This structure separates business truth, analytical features, machine learning,
and prediction output so that each stage can be tested and understood
independently.

## Project Components

### Synthetic Data Generation

The Generation Engine creates a realistic synthetic e-commerce environment
containing customers, products, categories, orders, order items, payments, and
shipments.

Business rules are applied during generation so that the resulting data behaves
like a connected business system rather than a collection of unrelated random
records.

### Quality Assurance

NorthStar uses dedicated QA processes to validate data integrity and certify
outputs before they are allowed to move downstream.

QA covers areas including relational integrity, financial reconciliation,
shipment consistency, privacy safeguards, feature behavior, business
interpretation, historical training observations, and machine learning inputs.

### Privacy Protection

The Privacy Engine separates customer identity from analytical behavior before
data enters the analytical pipeline.

Customer identifiers are replaced with dataset-scoped anonymous keys, allowing
behavior to remain traceable within the dataset without exposing the original
customer identity to downstream analytical and machine learning processes.

Customer timelines are also shifted using dataset-scoped temporal offsets while
preserving the relative timing of each customer's events. Safe offset limits
prevent shifted event dates from extending beyond the permitted temporal
boundary.

### Feature Engineering

Feature Engineering transforms purchase history into measurable behavioral
signals.

Features describe customer recency, purchase cadence, order behavior,
consistency, behavioral change, and deviation from the customer's own
historical purchasing pattern.

### Business Interpretation

The Business Interpretation layer converts analytical features into
business-readable customer purchase health.

Each customer is evaluated against their own purchasing history rather than a
single global definition of healthy behavior.

### Machine Learning

NorthStar creates historical point-in-time observations and future outcome
labels while protecting against future-data leakage.

The machine learning pipeline uses chronological training, validation, embargo,
and final test periods to preserve temporal integrity.

The final model estimates the probability that an eligible customer will become
**At Risk or Critical within the next 30 days**.

### Prediction Output

Prediction results contain the customer's anonymous key, observation date,
predicted probability, and binary risk classification.

These outputs are designed to support downstream retention analysis and
business decision-making without allowing the model itself to determine the
appropriate customer action.

## Purchase Health Engine

NorthStar evaluates customer health relative to each customer's own historical
purchase behavior rather than comparing every customer against a single global
standard.

The core idea is simple:

> **A customer's normal purchasing behavior establishes the baseline used to
> determine whether their current behavior is changing.**

NorthStar uses features such as `DaysSinceLastPurchase`,
`AverageDaysBetweenPurchases`, purchase interval consistency, and behavioral
change to interpret the customer's current purchase health.

### Healthy Window

A customer's expected purchase window is based on their historical average
purchase interval.

The upper boundary of the healthy window is:

```text
HealthyWindowDays = AverageDaysBetweenPurchases × 1.20
```

This provides a 20% tolerance beyond the customer's historical purchasing
cadence before deterioration begins affecting the Purchase Health Score.


<div align="center">

### Purchase Health Tiers

<table>
  <tr>
    <th>Purchase Health Score</th>
    <th>Tier</th>
  </tr>
  <tr>
    <td align="right">95–100</td>
    <td><strong>Healthy</strong></td>
  </tr>
  <tr>
    <td align="right">80–&lt;95</td>
    <td><strong>Watch</strong></td>
  </tr>
  <tr>
    <td align="right">60–&lt;80</td>
    <td><strong>At Risk</strong></td>
  </tr>
  <tr>
    <td align="right">0–&lt;60</td>
    <td><strong>Critical</strong></td>
  </tr>
  <tr>
    <td align="right">Unavailable</td>
    <td><strong>Insufficient History</strong></td>
  </tr>
</table>

</div>

Customers without enough evidence to calculate purchase health remain
Insufficient History rather than being assigned an artificial score.

This creates a business-readable interpretation of customer behavior that can
be used independently for analysis and also serves as the business truth
behind NorthStar's machine learning target.

## Predictive Modeling

NorthStar's machine learning model is designed to answer a specific business
question:

> **Will this customer be At Risk or Critical 30 days from now?**

### Target Definition

Historical observations are created using only information that would have been
available on the observation date.

For each eligible observation, NorthStar evaluates the customer's purchase
health 30 days later.

The modeling target, `AtRiskOrCriticalWithin30Days`, is assigned:

- `1` when the future customer state is **At Risk** or **Critical**
- `0` otherwise

Customers already classified as **Critical** at the observation date are
excluded from the prediction population.

### Temporal Protection

NorthStar uses chronological model-development periods rather than randomly
splitting historical observations.

<div align="center">
<pre>
Historical Observations
↓
Training Period
↓
Embargo
↓
Validation Period
↓
Embargo
↓
Final Test Period
</pre>
</div>

Embargo periods help protect the boundaries between datasets when the prediction
target looks 30 days into the future.

The final test dataset remains isolated from model development and threshold
selection so that it represents genuinely unseen future data.

### Classification Threshold

NorthStar uses a classification threshold of:

**`0.325`**

The threshold was selected using temporally protected validation data based on
the business tradeoff between identifying customers likely to deteriorate and
avoiding excessive retention-team alert volume.

False negatives were treated as the more costly error because failing to
identify a customer who later becomes At Risk or Critical may prevent the
business from intervening while an opportunity still exists.

The threshold therefore prioritizes class-1 recall rather than simply accepting
the default `0.50` classification threshold.

## Technology Stack

| Technology           | Role in NorthStar                                                                                           |
| -------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Python**           | Data generation, privacy processing, feature engineering, QA, business interpretation, and machine learning |
| **pandas**           | Data transformation, historical observations, feature datasets, and analytical processing                   |
| **scikit-learn**     | Machine learning model training, probability prediction, and model evaluation                               |
| **SQL / SQL Server** | Customer behavior analysis and development of the original Purchase Health Engine                           |
| **Decimal**          | Deterministic monetary calculations and financial rounding                                                  |
| **CSV**              | Portable datasets exchanged between major pipeline stages                                                   |
| **Git / GitHub**     | Version control, project history, and portfolio repository                                                  |
| **VS Code**          | Primary development environment                                                                             |

## Project Structure

The NorthStar repository separates generation, interpretation, machine learning,
quality assurance, configuration, documentation, and generated data into
clearly defined areas.


```text
Project NorthStar
├── data
│   ├── predictions
│   ├── privacy_filtered
│   ├── raw
│   ├── training
│   ├── training_dataset
│   └── training_source
│
├── docs
│   ├── Architecture
│   ├── ERD
│   ├── Reference
│   ├── Screenshots
│   └── Standards
│
├── python
│   ├── archive
│   ├── generators
│   ├── Interpretation
│   ├── machine_learning
│   ├── utilities
│   └── run_feature_pipeline.py
│
├── sql
│   ├── 00_setup
│   └── 02_business_analysis
│
└── README.MD
```

### Python Components

The active Python codebase includes:

- **Generation Engine** — creates the synthetic e-commerce environment.
- **QA Engine** — validates relational, financial, and operational integrity.
- **Privacy Engine** — removes direct customer identity from analytical data.
- **Privacy Engine QA** — validates privacy-preserving temporal safeguards.
- **Feature Engineering** — converts purchase history into behavioral features.
- **Feature QA** — validates engineered feature behavior.
- **Business Interpretation** — converts analytical features into Purchase Health.
- **Business Interpretation QA** — validates Purchase Health behavior.
- **Training Population Generator** — creates the historical business population.
- **ML Training Dataset Generator** — creates point-in-time observations and future targets.
- **ML Training Dataset QA** — validates historical observations and labels.
- **Machine Learning Engine** — performs temporal splitting, model training, evaluation, thresholding, and prediction.
- **Machine Learning Engine QA** — validates ML inputs, temporal boundaries, and model-development datasets.
- **Feature Pipeline Runner** — orchestrates feature generation, validation, and approved output.

## Documentation

NorthStar includes dedicated documentation covering the business, architectural,
engineering, and implementation decisions behind the project.

| Document                                                             | Purpose                                                                                             |
| -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [Architecture](docs/Architecture/Architecture.md)                    | Describes NorthStar's major components, responsibilities, data flow, and system boundaries.         |
| [Business Rules](docs/Reference/BusinessRules.md)                    | Defines the authoritative business logic used throughout the platform.                              |
| [Data Dictionary](docs/Reference/Data_Dictionary.md)                 | Documents datasets, fields, data types, relationships, and analytical meaning.                      |
| [Function Inventory](docs/Reference/NorthStar_Function_Inventory.md) | Provides a reference map of the active Python functions across the project.                         |
| [Engineering Standards](docs/Standards/Engineering_standards.md)     | Records approved reusable engineering standards and implementation decisions.                       |
| [Financial Standard](docs/Standards/Financial_Standard.md)           | Defines NorthStar's monetary representation, precision, rounding, calculation, and QA requirements. |
| [Issue Log](docs/Reference/Issue%20Log.md)                           | Records significant engineering issues, investigations, resolutions, and lessons learned.           |

Together, these documents provide traceability from the original business
problem through architecture, implementation, QA, and predictive modeling.

## Key Engineering Decisions

NorthStar was built around several deliberate engineering and analytical
decisions.

### Business Truth Before Machine Learning

The Purchase Health Engine was defined before predictive modeling began.

The machine learning model therefore learns to anticipate an established
business outcome rather than defining what customer risk means.

> **Business rules define the truth. Functions implement the rules. QA certifies
> the implementation.**

### Point-in-Time Data Integrity

Historical observations use only information that would have been available on
the observation date.

Future information is used only to determine supervised learning outcomes and
is never included as observation evidence.

### Privacy by Design

Direct customer identity is removed before analytical and machine learning
processing.

Anonymous customer keys preserve the relationships required for analysis
without allowing customer identity to become a model feature.

Temporal shifting further protects the original customer timeline while
preserving the relative event relationships required for behavioral analysis.

### Missing Data Preserves Meaning

When there is insufficient purchase history to calculate a behavioral feature,
NorthStar preserves the value as missing rather than replacing it with an
artificial zero or sentinel value.

This distinguishes **"no measurable value"** from a legitimate measured value
of zero.

### Financial Determinism

Financial calculations use `Decimal`, two-decimal monetary precision, and
`ROUND_HALF_UP` rounding.

Generation and QA follow the same financial standard so monetary values can be
reconciled deterministically.

### Temporal Model Development

Machine learning datasets are separated chronologically rather than through a
random train/test split.

Embargo periods protect dataset boundaries, validation data supports model and
threshold decisions, and the final test period remains isolated until final
evaluation.

### Business-Driven Classification Threshold

NorthStar uses a `0.325` classification threshold selected from temporally
protected validation results.

The threshold reflects the business cost of missed future At Risk or Critical
customers while also considering the operational workload created by false
positive retention alerts.

## Model Results

NorthStar evaluates model performance with emphasis on identifying customers
who will become At Risk or Critical within the 30-day prediction horizon.
Validation results were used for model-development and threshold decisions,
while the isolated Final Test population was reserved for final evaluation.

Because a missed deteriorating customer represents the more costly business
error, class-1 recall is treated as a primary model-selection metric.

### Validation Performance at Selected Threshold

At the selected `0.325` classification threshold, temporally protected
validation produced approximately:

<div align="center">

<table>
  <tr>
    <th>Metric</th>
    <th>Result</th>
  </tr>
  <tr>
    <td><strong>Recall</strong></td>
    <td align="right"><strong>72.35%</strong></td>
  </tr>
  <tr>
    <td><strong>Precision</strong></td>
    <td align="right"><strong>60.97%</strong></td>
  </tr>
  <tr>
    <td><strong>True Positives</strong></td>
    <td align="right"><strong>3,946</strong></td>
  </tr>
  <tr>
    <td><strong>False Negatives</strong></td>
    <td align="right"><strong>1,508</strong></td>
  </tr>
  <tr>
    <td><strong>False Positives</strong></td>
    <td align="right"><strong>2,526</strong></td>
  </tr>
  <tr>
    <td><strong>True Negatives</strong></td>
    <td align="right"><strong>21,052</strong></td>
  </tr>
</table>

</div>

These results represent the operating tradeoff used to select NorthStar's
v1.0 classification threshold.

The objective was not to find a mathematically perfect threshold. The selected
operating point balances the ability to identify future At Risk or Critical
customers against the retention-team workload created by false positive alerts.

The threshold was selected using validation data before evaluation against the
isolated final test period.

### Final Test Performance

After the `0.325` classification threshold was locked, the completed model was
evaluated against the isolated Final Test population.

<div align="center">
<table>
  <tr>
    <th>Metric</th>
    <th>Result</th>
  </tr>
  <tr>
    <td><strong>Recall</strong></td>
    <td align="right"><strong>77.23%</strong></td>
  </tr>
  <tr>
    <td><strong>Precision</strong></td>
    <td align="right"><strong>72.23%</strong></td>
  </tr>
  <tr>
    <td><strong>True Positives</strong></td>
    <td align="right"><strong>12,678</strong></td>
  </tr>
  <tr>
    <td><strong>False Negatives</strong></td>
    <td align="right"><strong>3,738</strong></td>
  </tr>
  <tr>
    <td><strong>False Positives</strong></td>
    <td align="right"><strong>4,875</strong></td>
  </tr>
  <tr>
    <td><strong>True Negatives</strong></td>
    <td align="right"><strong>49,492</strong></td>
  </tr>
</table>

</div>

These results represent final evaluation performance and were not used to
retune the classification threshold or make additional model-development
decisions.

## Getting Started

NorthStar is designed as a staged analytical pipeline rather than a single
monolithic application.

Each major stage can be executed and validated independently, allowing the
output of one stage to be inspected before it becomes the input to the next.

### General Workflow

<div align="center">
<pre>
Generate Business Data
↓
Run Data QA
↓
Generate Privacy-Protected Data
↓
Generate Features
↓
Validate Features
↓
Apply Business Interpretation
↓
Validate Business Interpretation
↓
Generate Historical ML Observations
↓
Validate Training Dataset
↓
Train and Evaluate Model
↓
Generate Predictions
</pre>
</div>

### Running the Project

NorthStar's Python components are organized by responsibility under the
`python/` directory.

Run the following commands from the `python/` directory.

```bash
python -m generators.generate_ecommerce_data
python -m utilities.qa_validation

python -m generators.generate_training_population
python -m utilities.privacy_engine
python -m utilities.privacy_engine_qa

python run_feature_pipeline.py
python -m utilities.feature_qa

python -m generators.ml_training_dataset_generator
python -m utilities.ml_training_dataset_qa

python -m machine_learning.machine_learning_engine
python -m machine_learning.machine_learning_engine_qa
```

The QA Engine is configured for the dataset being certified. Before running
`python -m utilities.qa_validation`, verify that the QA dataset selection
matches the intended operational or training dataset.

Before running the project:

1. Configure the required dataset paths and generation settings.
2. Generate or select the appropriate NorthStar dataset.
3. Run the applicable QA process before allowing data to move downstream.
4. Continue through the analytical and machine learning pipeline only after
   the preceding stage has passed validation.

NorthStar follows a fail-closed philosophy where practical: data that does not
pass its required validation should not be treated as certified downstream
input.

> **Do not bypass QA to make the pipeline pass. Investigate the failure,
> determine the cause, and correct the underlying issue.**

## Project Status

**NorthStar Commerce v1.0 — Portfolio Release**

The portfolio version of Project NorthStar is feature-complete.

The system includes synthetic business data generation, data quality assurance,
privacy protection, feature engineering, business interpretation, historical
machine learning dataset generation, temporal model development, threshold
selection, and customer risk prediction.

The complete NorthStar pipeline has passed final end-to-end verification and
release certification. All applicable QA stages passed against the final
generated datasets, and the isolated Final Test evaluation was completed
without using the Final Test population for model or threshold development.

Remaining release work is limited to final documentation review and repository
cleanup before the portfolio release is committed.

## What This Project Demonstrates

Project NorthStar demonstrates the ability to take a business problem from
initial definition through data engineering, analytical interpretation,
machine learning, validation, and operational output.

The project demonstrates practical experience with:

- Translating a business question into measurable analytical requirements
- Designing relational synthetic data with connected business behavior
- Building reusable data quality and QA processes
- Defining and enforcing financial calculation standards
- Designing privacy-conscious analytical pipelines
- Engineering behavioral features from historical transaction data
- Separating business rules from their technical implementation
- Building point-in-time historical datasets without future-data leakage
- Designing supervised machine learning targets from business outcomes
- Using chronological training, validation, embargo, and test periods
- Evaluating classification errors according to business cost
- Selecting a classification threshold based on validation evidence and
  operational tradeoffs
- Producing business-readable predictions rather than model output in isolation
- Documenting architecture, business rules, engineering standards, functions,
  datasets, and significant engineering decisions
- Using QA failures as evidence to investigate underlying system behavior rather
  than weakening validation to force a passing result

NorthStar reflects a development philosophy that became increasingly important
throughout the project:

> **Every feature is the answer to a business question.**

That principle connects the project's business requirements, feature
engineering, interpretation, machine learning, and QA into a single traceable
analytical system.

## Project History

Project NorthStar began on **July 25, 2026** as a portfolio project focused on
building a realistic e-commerce dataset for SQL and business analytics.

As development progressed, the project evolved into a larger end-to-end
analytical system incorporating data generation, QA, privacy protection,
behavioral feature engineering, customer purchase health interpretation,
historical machine learning observations, predictive modeling, and operational
risk outputs.

The project's direction was shaped by the business questions discovered during
development rather than by a predetermined list of technologies or features.

---

## Author

**Mat Thompson**

Project NorthStar was designed and developed as a portfolio project demonstrating
practical data analytics, Python, SQL, data engineering, quality assurance, and
machine learning skills.

The project emphasizes understanding and documenting not only **what** the
system does, but **why** each component exists and how it contributes to the
business objective.

---

<div align="center">

### Project NorthStar

**Business Question → Feature → Business Rules → Function → QA**

*Follow the behavior. Find the signal. Anticipate the change.*

</div>