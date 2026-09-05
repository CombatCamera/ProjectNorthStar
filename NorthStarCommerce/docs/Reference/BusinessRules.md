# NorthStar Commerce Business Rules

## Purpose

This document defines the business rules that govern NorthStar Commerce behavior,
customer purchase-health interpretation, historical machine learning labels,
and operational prediction decisions.

Business rules describe what NorthStar considers valid or meaningful business
behavior. They are separate from the code that implements them and the QA that
validates them.

> **Business rules define the truth. Functions implement the rules. QA certifies the implementation.**

## Customer Shopping Profiles

Each customer is assigned a Shopping Profile that represents their expected purchasing behavior throughout the year.

| Profile | Distribution | Expected Orders Per Year |
|----------|-------------:|-------------------------:|
| Occasional | 35% | 1–3 |
| Regular | 40% | 4–8 |
| Frequent | 20% | 9–18 |
| VIP | 5% | 19–35 |

Shopping Profiles are independent of Customer Segment and Loyalty Tier. This allows realistic variation in customer behavior and supports downstream analytics including:

- Customer Lifetime Value (CLV)
- Repeat Purchase Rate
- Customer Retention
- Revenue Distribution
- Purchase Frequency Analysis
  
## Successful Purchase Rule

NorthStar Commerce measures customer purchase behavior using successful
purchases.

A purchase is considered successful when the associated payment reaches a
successful payment status.

Orders without a successful payment are excluded from successful purchase
history and therefore do not contribute to purchase-health behavior.

### Successful Purchase History

Successful purchase history is the approved behavioral foundation for
downstream purchase-health analysis.

It is used to determine:

- Purchase recency
- Purchase intervals
- Successful order count
- Average order value
- Purchase frequency
- Purchase timing behavior

### Business Rule

> **Only successful purchases contribute to measured customer purchase behavior.**

## Purchase Health Eligibility Rule

A customer becomes eligible for Purchase Health evaluation after completing at
least one successful purchase.

Customers without a successful purchase are excluded from the Purchase Health
population because no successful purchase behavior exists to evaluate.

### Eligibility

```text
At Least One Successful Purchase?
    ├── No  → Excluded from Purchase Health Population
    └── Yes → Included in Purchase Health Population
```

Eligibility does not guarantee that enough purchase history exists to calculate
every Purchase Health feature.

Customers may enter the Purchase Health population while still having
insufficient history for features that require multiple purchases or purchase
intervals.

### Business Rule

> **Purchase Health begins when successful purchase behavior begins.**

## Point-in-Time Business Rule

Historical customer behavior must be calculated using only business information
that existed on or before the applicable `ObservationDate`.

For purchase behavior, a successful purchase may contribute to a historical
observation only when:

`OrderDateTime` <= `ObservationDate`

Purchases occurring after the observation date are future information and must
not contribute to the customer's historical features or observation-time
Purchase Health interpretation.

### Future Outcome Information

Future information may be examined after the observation date when determining
the supervised machine learning outcome.

This future information is used only to establish what happened to the customer
after the observation and must not be included in the evidence presented to the
model.

### Business Rule

> **NorthStar may use the future to determine what happened, but never to change what was known at the observation date.**

## Purchase Interval Rules

NorthStar measures customer purchase timing using the number of days between
consecutive successful purchases.

Only successful purchases belonging to the same customer may be used to
construct that customer's purchase intervals.

### Purchase Interval

For two consecutive successful purchases:

`DaysBetweenPurchases = CurrentPurchaseDate - PreviousPurchaseDate`

The first successful purchase does not have a purchase interval because no
previous successful purchase exists for comparison.

### Average Purchase Interval

`AverageDaysBetweenPurchases` represents the customer's typical historical
purchase interval.

It is calculated from the customer's available purchase intervals rather than
from the total age of the customer relationship.

### Purchase Interval Change

NorthStar also measures how consecutive purchase intervals change over time.

`PurchaseIntervalChange = CurrentPurchaseInterval - PreviousPurchaseInterval`

A positive change means the customer's purchase interval became longer.

A negative change means the customer's purchase interval became shorter.

A zero change means the purchase interval remained unchanged.

The first available purchase interval does not have an interval change because
no previous interval exists for comparison.

### Business Rule

> **Purchase timing is measured from successful purchase to successful purchase.**
> 
## Reliable Purchase History Rule

Some behavioral features require more historical evidence than basic Purchase
Health eligibility.

NorthStar v1.0 requires a minimum of 10 purchase intervals before purchase
history is considered sufficiently reliable for behavior features that depend
on established interval patterns.

### Reliability Threshold

`MinimumReliablePurchaseIntervals = 10`

Customers below this threshold remain valid members of the Purchase Health
population, but behavior features requiring reliable interval history remain
missing until sufficient evidence exists.

NorthStar does not replace this missing evidence with zero.

A value of zero would represent an observed behavioral result, while a missing
value represents insufficient evidence to calculate that result reliably.

### Current Features Requiring Reliable History

The reliability threshold currently applies to:

- `PurchaseIntervalStdDev`
- `AverageIntervalChange`

### Business Rule

> **Insufficient evidence remains insufficient evidence; it does not become zero.**

## Purchase Interval Variability Rule

NorthStar measures the consistency of a customer's purchase timing using
`PurchaseIntervalStdDev`.

The feature measures how much the customer's historical purchase intervals
vary around their average purchase interval.

### Business Interpretation

A lower `PurchaseIntervalStdDev` indicates more consistent purchase timing.

A higher `PurchaseIntervalStdDev` indicates greater variation in purchase
timing.

A value of zero represents perfectly consistent observed purchase intervals.

A missing value represents insufficient reliable purchase history and therefore
has a different business meaning from zero.

### Calculation Eligibility

`PurchaseIntervalStdDev` is calculated only when the customer satisfies
NorthStar's Reliable Purchase History Rule.

Until that requirement is satisfied, the feature remains missing.

### Business Rule

> **Purchase interval variability measures consistency of timing, not whether the timing itself is healthy or unhealthy.**

## Average Interval Change Rule

NorthStar measures the overall direction of change in a customer's purchase
timing using `AverageIntervalChange`.

The feature represents the average change between consecutive purchase
intervals.

### Business Interpretation

A positive `AverageIntervalChange` indicates that purchase intervals are
becoming longer on average.

A negative `AverageIntervalChange` indicates that purchase intervals are
becoming shorter on average.

A value near zero indicates that purchase intervals show little average
directional change.

A missing value represents insufficient reliable purchase history and is not
equivalent to zero.

### Calculation Eligibility

`AverageIntervalChange` is calculated only when the customer satisfies
NorthStar's Reliable Purchase History Rule.

Until that requirement is satisfied, the feature remains missing.

### Business Rule

> **Average interval change measures the direction of purchasing rhythm over time, not the variability of that rhythm.**

## Days Since Last Purchase Rule

NorthStar measures customer purchase recency using `DaysSinceLastPurchase`.

The feature represents the number of days between the customer's most recent
successful purchase and the applicable evaluation date.

For historical observations, the evaluation date is the `ObservationDate`.

### Business Interpretation

A lower `DaysSinceLastPurchase` indicates that the customer's most recent
successful purchase occurred more recently.

A higher `DaysSinceLastPurchase` indicates a longer period of inactivity since
the customer's most recent successful purchase.

The value is interpreted relative to the customer's own historical purchasing
behavior rather than against a universal inactivity threshold.

### Historical Rule

When calculating `DaysSinceLastPurchase` for a historical observation, only
successful purchases occurring on or before the `ObservationDate` may be
considered.

Purchases occurring after the observation date cannot change the historical
recency value.

### Business Rule

> **Purchase recency becomes meaningful when compared with the customer's own purchasing rhythm.**

## Healthy Window Rule

NorthStar evaluates customer purchase recency relative to the customer's own
historical purchasing rhythm.

The Healthy Window represents the expected range around the customer's
`AverageDaysBetweenPurchases`.

### Healthy Window

NorthStar v1.0 uses a tolerance of ±20% around the customer's average purchase
interval.

```text
Lower Healthy Boundary = AverageDaysBetweenPurchases × 0.80

Upper Healthy Boundary = AverageDaysBetweenPurchases × 1.20
```

For Purchase Health evaluation, HealthyWindowDays represents the upper
boundary of that expected purchase window.

```text
HealthyWindowDays = AverageDaysBetweenPurchases × 1.20
```

### Business Interpretation

A customer whose inactivity remains within the Healthy Window is behaving
within the expected timing of their historical purchase pattern.

Once `DaysSinceLastPurchase` exceeds `HealthyWindowDays`, the customer has moved
beyond the expected purchase window.

The significance of that delay is determined by how far beyond the Healthy
Window the customer has progressed.

### Business Rule

> **Purchase health is evaluated against the customer's own historical purchasing rhythm rather than a universal inactivity threshold.**

## Percent Beyond Healthy Window Rule

NorthStar measures the degree to which customer inactivity has exceeded the
expected Healthy Window using `PercentBeyondHealthyWindow`.

The feature compares `DaysSinceLastPurchase` with the customer's
`HealthyWindowDays`.

### Business Interpretation

When `DaysSinceLastPurchase` has not exceeded `HealthyWindowDays`, the customer
is not beyond the expected purchase window.

When `DaysSinceLastPurchase` exceeds `HealthyWindowDays`,
`PercentBeyondHealthyWindow` measures the size of that delay relative to the
customer's own Healthy Window.

```text
PercentBeyondHealthyWindow =
    (DaysSinceLastPurchase - HealthyWindowDays) / HealthyWindowDays
```

A larger positive value represents a greater departure from the customer's
expected purchasing rhythm.

### Example

If a customer's `HealthyWindowDays` is 30 days and the customer has not made a
successful purchase for 45 days:

```text
(45 - 30) / 30 = 0.50
```

The customer is therefore 50% beyond their Healthy Window.

### Business Rule

> **NorthStar measures purchase delay relative to how late the customer is for their own expected purchasing rhythm.**

## Purchase Health Score Rule

NorthStar converts the customer's position relative to their Healthy Window
into `PurchaseHealthScore`.

The score provides a standardized representation of the customer's current
purchase health based on their own historical purchasing rhythm.

### Business Interpretation

A higher `PurchaseHealthScore` represents healthier purchase behavior.

As customer inactivity progresses beyond the expected Healthy Window,
`PurchaseHealthScore` decreases.

The score therefore converts purchase delay into a form that can be used
consistently by downstream Business Interpretation.

### Customer-Specific Context

`PurchaseHealthScore` is not based on a universal number of inactive days.

The score is derived from evidence that has already been normalized against the
customer's own expected purchasing behavior.

This allows customers with different purchasing rhythms to be evaluated using
the same Purchase Health framework.

### Business Rule

> **Purchase Health Score represents the customer's current purchase health relative to their own established purchasing behavior.**

## Purchase Health Score Calculation

NorthStar calculates `PurchaseHealthScore` from the customer's
`PercentBeyondHealthyWindow`.

### Score Calculation

When the customer has not moved beyond the Healthy Window:

```text
PercentBeyondHealthyWindow = 0
PurchaseHealthScore = 100
```
Once the customer moves beyond the Healthy Window:

```text
PurchaseHealthScore =
    100 - (PercentBeyondHealthyWindow × 100)
```

The score is bounded between 0 and 100.

When `PercentBeyondHealthyWindow` reaches or exceeds 1.0, representing 100%
beyond the Healthy Window:

```text
PurchaseHealthScore = 0
```

When the required purchase-history evidence does not exist,
`PurchaseHealthScore` remains missing and the customer is interpreted as
having Insufficient History.

### Score Direction

|Purchase Health Score|	Meaning|
|---:|---|
|Higher	|Healthier relative to the customer's expected purchase rhythm|
|Lower|	Further beyond the customer's expected purchase rhythm|
|100|	Customer has not exceeded the Healthy Window|
|0|	Customer has reached or exceeded 100% beyond the Healthy Window|

### Business Rule
> **Purchase Health Score decreases as customer inactivity progresses beyond the customer's expected purchase window,**

## Purchase Health Tier Rules

NorthStar converts `PurchaseHealthScore` into a defined Purchase Health Tier.

The tier provides a business-readable interpretation of the customer's current
purchase health.

### Tier Thresholds

| Purchase Health Tier | Purchase Health Score |
| -------------------- | --------------------: |
| Healthy              |                95–100 |
| Watch                |                80–<95 |
| At Risk              |                60–<80 |
| Critical             |                 0–<60 |
| Insufficient History |     Score unavailable |

### Tier Interpretation

**Healthy** represents customer behavior that remains consistent with the
customer's expected purchasing rhythm.

**Watch** represents an early departure from expected purchasing behavior that
warrants awareness but has not yet reached At Risk status.

**At Risk** represents a meaningful deterioration from the customer's expected
purchasing rhythm.

**Critical** represents a severe departure from the customer's expected
purchasing rhythm.

**Insufficient History** represents a customer for whom the required historical
evidence does not yet exist to produce a valid Purchase Health Score.

### Business Rule

> **Purchase Health tiers convert numerical purchase-health evidence into consistent business meaning.**

## 30-Day Prediction Target Rule

NorthStar's machine learning target answers the business question:

> **Will this customer be At Risk or Critical 30 days from the observation date?**

The supervised learning target is:

`AtRiskOrCriticalWithin30Days`

### Eligible Observation Population

Training observations are eligible for the prediction target when the
customer's `ObservationPurchaseHealthTier` is:

- Healthy
- Watch
- At Risk

Observations where the customer is already Critical are excluded from the
prediction population.

### Target Outcome

After the 30-day prediction horizon, NorthStar evaluates the customer's
`OutcomePurchaseHealthTier`.

```text
OutcomePurchaseHealthTier
        ↓
At Risk or Critical?
    ├── No  → AtRiskOrCriticalWithin30Days = 0
    └── Yes → AtRiskOrCriticalWithin30Days = 1
```

A target value of `1` means the customer is At Risk or Critical at the future
outcome point.

A target value of `0` means the customer is not At Risk or Critical at the
future outcome point.

### Important Distinction

The target does not ask whether the customer's Purchase Health Tier changed.

It asks whether the customer is At Risk or Critical at the defined future
outcome point.

For example, a customer who is already At Risk at the observation date may
remain At Risk 30 days later and still receive a target value of 1.

### Business Rule

> **The model predicts future At Risk or Critical status, not simply whether customer health changed.**

## Prediction Error Cost and Decision Threshold Rule

NorthStar does not treat all machine learning prediction errors as having equal
business cost.

For the Customer Purchase Health prediction problem, a false negative is
considered more costly than a false positive.

### Error Cost

A false negative occurs when NorthStar predicts that a customer will not be At
Risk or Critical, but the customer actually reaches one of those states within
the prediction horizon.

This error represents a missed opportunity for the business to identify a
customer whose purchase health requires attention.

A false positive occurs when NorthStar flags a customer as likely to become At
Risk or Critical, but the customer does not reach one of those states.

False positives create unnecessary operational workload and therefore cannot
be ignored.

### Model Evaluation Priority

Because false negatives carry the greater business cost, NorthStar prioritizes
recall for the positive class when evaluating the model.

Accuracy alone is not sufficient for evaluating this prediction problem because
the target population is imbalanced and a high accuracy score can conceal poor
identification of customers who actually become At Risk or Critical.

### Decision Threshold

NorthStar v1.0 uses:

`MODEL_DECISION_THRESHOLD = 0.325`

A predicted probability greater than or equal to the threshold produces a
positive operational prediction.

```text
AtRiskOrCriticalProbability >= 0.325
    ├── No  → PredictedAtRiskOrCritical = False
    └── Yes → PredictedAtRiskOrCritical = True
```

The threshold was selected using the temporally protected validation dataset
before evaluation against the final test dataset.

Lower thresholds increase the model's ability to identify positive outcomes but
also increase false-positive operational workload.

Higher thresholds reduce false-positive workload but increase the risk of
missing customers who become At Risk or Critical.

### Business Rule

> **NorthStar prioritizes identifying future customer risk while keeping unnecessary operational intervention at a reasonable level.**

## Temporal Model Development Rule

NorthStar develops and evaluates machine learning models using chronological
data separation rather than randomly mixing historical observations across
training, validation, and final testing populations.

### Dataset Responsibilities

| Dataset            | Business Purpose                                                                          |
| ------------------ | ----------------------------------------------------------------------------------------- |
| Training           | Teaches the model relationships between historical customer evidence and future outcomes. |
| Validation Embargo | Separates training observations from the validation period.                               |
| Validation         | Supports model-development decisions, including decision-threshold selection.             |
| Final Test Embargo | Separates model-development observations from the final test period.                      |
| Final Test         | Measures performance after model-development decisions have been locked.                  |

### Development Boundary

The final test population must not be used to select the model's decision
threshold or make other model-development decisions.

NorthStar v1.0 selects its decision threshold using the validation population
and locks that threshold before final test evaluation.

Embargo periods provide additional temporal separation around the validation
and final test boundaries.

### Business Reason

NorthStar's prediction problem asks the model to anticipate future customer
purchase health.

Model evaluation must therefore represent the same fundamental challenge:
learn from earlier customer behavior and predict outcomes occurring later in
time.

### Business Rule

> **Future evaluation data may judge the model, but it may not teach the model how to pass the test.**

## Prediction Output and Traceability Rule

NorthStar preserves enough information with each machine learning prediction to
identify the customer observation that produced the prediction without exposing
customer identity to the model.

### Required Prediction Output

Each historical prediction contains:

| Field                         | Business Purpose                                                                               |
| ----------------------------- | ---------------------------------------------------------------------------------------------- |
| `AnonymousCustomerKey`        | Identifies the anonymous customer associated with the prediction.                              |
| `ObservationDate`             | Identifies the point in time represented by the prediction.                                    |
| `AtRiskOrCriticalProbability` | Represents the model's estimated probability of an At Risk or Critical outcome within 30 days. |
| `PredictedAtRiskOrCritical`   | Represents the operational prediction after applying the decision threshold.                   |

### Identity Boundary

`AnonymousCustomerKey` is retained for traceability but is not supplied to the
model as behavioral evidence.

The model therefore learns from approved customer behavior features rather than
from the customer's identifier.

### Probability and Prediction

`AtRiskOrCriticalProbability` and `PredictedAtRiskOrCritical` represent two
different pieces of information.

The probability records the model's estimated risk.

The prediction records the business decision produced by applying NorthStar's
decision threshold to that probability.

### Historical Meaning

A prediction represents the model's assessment of a customer at a specific
`ObservationDate`.

It does not represent a permanent classification of that customer.

As customer behavior changes over time, later observations may produce
different probabilities and prediction outcomes.

### Business Rule

> **A NorthStar prediction belongs to a customer observation at a point in time, not permanently to the customer.**

## Operational Prediction Boundary

NorthStar machine learning predictions provide evidence that may support future
customer-retention and operational decision-making.

A positive prediction indicates that the model estimates the customer has met
NorthStar's defined probability threshold for becoming At Risk or Critical
within the 30-day prediction horizon.

### Positive Prediction Meaning

```text
PredictedAtRiskOrCritical = True
                ↓
Customer Exceeds Prediction Threshold
                ↓
Potential Operational Attention
```

A positive prediction does not establish that the customer will definitely
become At Risk or Critical.

It represents elevated predicted risk based on the customer's available
behavioral evidence.

### Operational Action

NorthStar Commerce v1.0 does not automatically determine or execute a customer
retention action from a prediction.

Future operational systems may use the prediction alongside other authorized
business information to support activities such as:

- Customer review
- Retention prioritization
- Alerts
- Dashboard monitoring
- Customer outreach workflows

The appropriate operational response remains separate from the machine learning
prediction itself.

### Business Rule

> **The model identifies predicted risk; the business determines the appropriate response.**

## Business Rule Ownership and Change Control

NorthStar treats documented business rules as the authoritative definition of
the business behavior that production logic is expected to implement.

A change to a business rule must be treated as a deliberate change to NorthStar
behavior rather than as an isolated code modification.

### Rule Change Flow

```text
    Business Requirement Changes
                ↓
    Business Rule Updated
                ↓
    Implementation Updated
                ↓
        QA Updated
                ↓
        Validation
                ↓
        Certification
```
When an implemented business rule changes, the corresponding QA must continue
to validate the intended behavior.

Documentation, implementation, and QA should describe the same business truth.

### Business Rule

> **Change the rule deliberately, implement it consistently, and certify the new behavior before accepting it as NorthStar truth.**


