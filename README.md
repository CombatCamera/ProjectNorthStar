# Project NorthStar

**A business-driven data analytics and machine learning platform designed to transform raw operational data into actionable insights and predictive decision support.**

Project NorthStar is an evolving analytics platform built around a simple principle:

> **Every feature is the answer to a business question.**

Rather than beginning with technology and searching for a use case, NorthStar begins with a business problem, defines the rules required to answer it, and then builds the data, analytics, engineering, and machine learning systems needed to support that decision.

## NorthStarCommerce

**NorthStarCommerce** is the first complete implementation of the Project NorthStar methodology.

It models an end-to-end e-commerce analytics environment, beginning with synthetic operational data and progressing through data validation, business-rule development, behavioral feature engineering, privacy-preserving analytics, and machine learning.

The system ultimately answers a practical business question:

> **Which customers are showing signs of deteriorating purchase health and may require proactive retention attention?**

NorthStarCommerce converts customer purchase behavior into measurable health indicators and uses those signals to predict whether a customer is likely to become **At Risk or Critical within the next 30 days**.

### Explore NorthStarCommerce

For the complete technical documentation, architecture, business rules, machine learning methodology, and project results, see the **[NorthStarCommerce README](NorthStarCommerce/README.md)**.

## What NorthStarCommerce Demonstrates

NorthStarCommerce was built as an end-to-end analytics system rather than a collection of isolated exercises. The project demonstrates how a business problem can be carried from raw data through engineering, analysis, prediction, validation, and documentation.

Key capabilities include:

- **Synthetic Data Engineering** — Generates realistic e-commerce customers, products, orders, payments, shipments, and behavioral history using defined business rules.

- **Data Quality & QA Engineering** — Uses reusable validation functions to test referential integrity, financial reconciliation, business rules, feature calculations, and generated datasets.

- **SQL Business Analysis** — Translates customer behavior into business-facing metrics and purchase-health classifications.

- **Behavioral Feature Engineering** — Builds temporal customer features such as purchase cadence, recency, interval variability, and changes in purchasing behavior.

- **Privacy-Preserving Analytics** — Separates personally identifiable information from analytical data using dataset-scoped anonymous customer identifiers and fail-closed privacy controls.

- **Machine Learning** — Predicts whether eligible customers will become **At Risk or Critical within 30 days** using temporally protected training, validation, and test data.

- **Business-Driven Model Evaluation** — Evaluates model thresholds according to the operational tradeoff between identifying customers at risk and controlling retention-team alert workload.

- **Technical Documentation** — Documents architecture, business rules, data definitions, engineering standards, QA decisions, and model methodology alongside the implementation.

## The NorthStar Methodology

NorthStar follows a business-first development process designed to keep technical work connected to a clearly defined purpose.

<div align="center">
<pre>
Business Question
↓
Feature (Answer)
↓
Business Rules
↓
Implementation
↓
QA & Validation
</pre>
</div>

Each analytical feature begins with a question the business needs answered. The required business rules are defined before implementation, and the resulting logic is validated before it becomes part of the analytical pipeline.

This approach helps keep the system explainable, testable, and aligned with the decision it was designed to support.

## Repository Architecture

Project NorthStar is organized as an expandable platform. Individual implementations can operate within the larger NorthStar methodology while maintaining their own data, code, documentation, and analytical workflows.

```text
ProjectNorthStar/
│
├── NorthStarCommerce/
│   ├── data/
│   ├── docs/
│   ├── python/
│   ├── sql/
│   └── README.md
│
├── docs/
├── shared-assets/
└── templates/
```

### NorthStarCommerce

The current production implementation of the NorthStar methodology and the primary focus of this repository.

### Shared NorthStar Resources

The root-level structure provides space for documentation, reusable assets, standards, and future implementations without requiring those components to be embedded directly inside NorthStarCommerce.

This architecture allows NorthStar to grow while keeping each implementation logically separated and independently understandable.

## Project Results

NorthStarCommerce progressed from synthetic operational data generation to a validated predictive customer-retention system.

The machine learning pipeline uses a **30-day prediction horizon** to identify eligible customers who may transition into an **At Risk or Critical** purchase-health state.

To reduce temporal leakage and better represent real-world deployment, model development uses time-based training, validation, embargo, and test periods rather than randomly mixing historical observations.

For the v1.0 operating point, NorthStarCommerce selected a classification threshold of **0.325** based on the business tradeoff between identifying future At Risk/Critical customers and limiting unnecessary retention-team alerts.

At that threshold, temporally protected validation produced approximately:

| Metric | Result |
| --- | ---: |
| Recall | 72.35% |
| Precision | 60.97% |
| True Positives | 3,946 |
| False Negatives | 1,508 |
| False Positives | 2,526 |
| True Negatives | 21,052 |

The threshold is not treated as a mathematically perfect cutoff. It represents a documented **business operating decision** that can be adjusted as retention capacity, intervention costs, or business priorities change.

Detailed model methodology, feature definitions, QA evidence, and implementation decisions are documented within **[NorthStarCommerce](NorthStarCommerce/README.md)**.

## Technology & Skills

NorthStarCommerce combines data engineering, analytics, machine learning, software engineering, and technical documentation within a single end-to-end project.

| Area | Technologies & Skills |
| --- | --- |
| Programming | Python |
| Data Analysis | pandas, NumPy |
| Machine Learning | scikit-learn, classification modeling, threshold evaluation |
| SQL | PostgreSQL, CTEs, analytical queries, business-rule implementation |
| Feature Engineering | Temporal features, behavioral metrics, purchase cadence, recency analysis |
| Data Engineering | Synthetic data generation, reusable pipelines, dataset validation |
| Data Quality | Automated QA, reconciliation testing, integrity checks, controlled test cases |
| Privacy Engineering | PII separation, anonymized identifiers, whitelist-based data access, fail-closed controls |
| ML Validation | Temporal splitting, embargo periods, leakage prevention, precision/recall analysis |
| Financial Data | Decimal-based monetary calculations and defined rounding standards |
| Version Control | Git, GitHub |
| Documentation | Markdown, architecture documentation, business rules, data dictionaries, engineering standards |

## Design Principles

NorthStar is built around a small set of principles that guide technical and analytical decisions throughout the project.

### Business Purpose Before Technology

Technical work begins with the problem that needs to be solved. Tools, models, and features are selected only after the business objective is understood.

### Every Feature Answers a Business Question

Features are not created simply because the data makes them possible. Each feature must provide information that supports a defined analytical or operational question.

### Prefer Clear and Maintainable Designs

> **Prefer the simplest design that remains clear, maintainable, and teachable.**

NorthStar favors explicit, understandable implementations over unnecessary complexity. Code and analytical logic should be explainable to the people responsible for maintaining, validating, and using the system.

### Validate Before Trusting

Generated data, financial calculations, behavioral features, privacy controls, and machine learning outputs are supported by QA processes designed to verify assumptions before downstream use.

### Privacy by Design

Personally identifiable information is separated from analytical workflows whenever it is not required. Analytical systems receive only the information explicitly permitted for their purpose.

### Business Decisions Remain Human Decisions

Predictive outputs are designed to support decision-making rather than replace it. Model scores identify patterns and prioritize attention; business teams retain responsibility for determining the appropriate action.

## Documentation

NorthStarCommerce includes detailed documentation covering the business, analytical, and engineering decisions behind the system.

Key documentation areas include:

- **[NorthStarCommerce Overview](NorthStarCommerce/README.md)** — Complete project walkthrough and technical overview.
- **Architecture** — System structure, data flow, and component responsibilities.
- **Business Rules** — Definitions and decision logic used throughout the analytical system.
- **Data Dictionary** — Dataset, field, and feature definitions.
- **Engineering Standards** — Technical standards established during development.
- **QA & Validation** — Validation methodology and evidence supporting data and feature reliability.
- **Machine Learning** — Feature generation, temporal validation, threshold selection, and model evaluation.

Detailed supporting documentation is available within [`NorthStarCommerce/docs`](NorthStarCommerce/docs/).

## Project Status

**NorthStarCommerce v1.0 — Complete**

The v1.0 implementation establishes the foundation of Project NorthStar and demonstrates the complete path from operational data generation through predictive decision support.

Project NorthStar is designed to remain extensible. Future implementations can build on the same business-first methodology, engineering standards, privacy principles, and validation approach established through NorthStarCommerce.