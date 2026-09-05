'''
===============================================================================
Project NorthStar
ML Training Dataset QA Engine
-------------------------------------------------------------------------------
Author: Mat Thompson
Created: 2026-08-26
Last Updated 2026-08-30
Version: 1.0

Purpose:
Validate the construction of NorthStar machine learning training datasets and
ensure that historical training examples follow the required temporal,
population, labeling, and data-leakage rules.

Business Objective:
Ensure that machine learning training data accurately represents what NorthStar
could have known at each historical observation date and that future outcomes
are used only to generate the correct training labels.

Core Responsibilities:
- Validate historical observation-date generation.
- Validate observation cadence.
- Validate prediction-horizon boundaries.
- Validate training population eligibility.
- Validate future outcome and target-label generation.
- Detect temporal data leakage.
- Validate assembled ML training datasets.
- Produce standardized PASS/FAIL QA results.
- Provide diagnostic information for failed validations.

Current QA Scope:
- Observation date generation.
- 7-day observation cadence.
- Full 30-day prediction horizon availability.
- Training population eligibility.
- Observation purchase-health validation.
- Outcome purchase-health validation.
- Target label validation.
- Historical feature reconciliation.
- Temporal leakage detection.
- Final ML training dataset certification.

QA Result Contract:
Each validation returns a standardized result containing:

    name
    passed
    records_checked
    issues_found
    details

Temporal Integrity Principle:
Feature evidence may contain only information available on or before the
observation date. Future information may be used only by the teacher to
determine the observed outcome and training label.

Engineering Principles:
- Every training-data rule must be testable.
- Controlled scenarios should have known expected outcomes.
- QA logic remains separate from training-dataset generation logic.
- Validation should fail clearly and provide useful diagnostic information.
- Temporal leakage must be treated as a blocking failure.
- QA results should follow a consistent reporting structure.
- Prefer the simplest design that remains clear, maintainable, and teachable.

Future Expansion:
This engine is designed to support additional training-dataset validations,
expanded label strategies, alternative prediction horizons, observation
cadences, model-ready dataset certification, and future NorthStar machine
learning workflows.
===============================================================================
'''
from datetime import timedelta
import pandas as pd

from generators.ml_training_dataset_generator import (
    generate_target_label,
    generate_observation_dates,
    OBSERVATION_FREQUENCY_DAYS,
    PREDICTION_HORIZON_DAYS,
    OUTPUT_DATA_PATH,
    TRAINING_FINAL_DATA_DATE,
)

# ==========================================
# Validation Functions
# ==========================================

def validate_observation_dates():

    issues = []

    start_date = pd.to_datetime("2025-01-01")
    
    final_data_date = pd.to_datetime("2025-02-28")

    observation_dates = generate_observation_dates(
        start_date,
        final_data_date,
    )

    if observation_dates[0] != start_date:
        issues.append("Observation date check failed.")

    observation_intervals = observation_dates.to_series().diff()
    
    actual_intervals = observation_intervals.dropna()
    
    expected_interval = timedelta(
        days=OBSERVATION_FREQUENCY_DAYS
    )
    
    if (actual_intervals != expected_interval).any():
        issues.append("Intervals do not match.")
        
    prediction_horizon = timedelta(
        days=PREDICTION_HORIZON_DAYS
    )
    
    last_observation_date = observation_dates[-1]
    
    if (last_observation_date + prediction_horizon > final_data_date):
        issues.append("Final Observation date does not meet prediction horizon.")
        
    passed = len(issues) == 0
    
    
    return {
    "name": "Observation Date Generation",
    "passed": passed,
    "records_checked": len(observation_dates),
    "issues_found": len(issues),
    "details": " | ".join(issues),
}


def validate_target_labels():
    
    issues = []
    
    purchase_health_comparison = pd.DataFrame({
        "AnonymousCustomerKey": [
            "HealthyToHealthy",
            "HealthyToWatch",
            "HealthyToAtRisk",
            "WatchToCritical",
            "CriticalToCritical",
            "InsufficientToCritical"
        ],
        "ObservationPurchaseHealthTier": [
            "Healthy",
            "Healthy",
            "Healthy",
            "Watch",
            "Critical",
            "Insufficient History",
        ],
        "OutcomePurchaseHealthTier": [
            "Healthy",
            "Watch",
            "At Risk",
            "Critical",
            "Critical",
            "Critical",
        ],
    })

    labeled_records = generate_target_label(
        purchase_health_comparison
    )
    
    if len(labeled_records) != 4:
        issues.append(f"Purchase Health comparison returned {len(labeled_records)} records; expected 4.")

    if "CriticalToCritical" in labeled_records[
        "AnonymousCustomerKey"
    ].values:
        issues.append(
            "Critical Observation record was not excluded."
        )

    if "InsufficientToCritical" in labeled_records[
        "AnonymousCustomerKey"
    ].values:
        issues.append(
            "Insufficient-history observation record was not excluded."
        )

    negative_records = labeled_records.loc[
        labeled_records["AnonymousCustomerKey"].isin(
            [
                "HealthyToHealthy",
                "HealthyToWatch",
            ]
        )
    ]
    
    if not (
        negative_records["AtRiskOrCriticalWithin30Days"] == 0
    ).all():
        issues.append(
            "Negative target labels were generated incorrectly."
        )


    positive_records = labeled_records.loc[
        labeled_records["AnonymousCustomerKey"].isin(
            [
                "HealthyToAtRisk",
                "WatchToCritical",
            ]
        )
    ]
    
    if not (
        positive_records["AtRiskOrCriticalWithin30Days"] == 1
    ).all():
        issues.append(
            "Positive target labels were generated incorrectly."
        )
        
    passed = len(issues) == 0
    
    return {
        "name": "Target Label Generation",
        "passed": passed,
        "records_checked": len(purchase_health_comparison),
        "issues_found": len(issues),
        "details": " | ".join(issues),
    }
  
        
def validate_training_target_labels(
    ml_training_dataset,
    final_data_date,
):
    
    issues = []
        
    # Missing target labels check
    if ml_training_dataset["AtRiskOrCriticalWithin30Days"].isna().any():
        issues.append("Missing value check failed.")
    
    
    # Invalid target value check (0 or 1)
    if (~ml_training_dataset["AtRiskOrCriticalWithin30Days"].isin(
        [0, 1]
    )).any():
        issues.append("Invalid target value check failed.")
        
        
    # Duplicate Customer key check   
    if ml_training_dataset.duplicated(
        subset=[
            "AnonymousCustomerKey",
            "ObservationDate",
        ]
    ).any():
        issues.append("Duplicate customer observation found.")
    
    
    # Purchase Health Tier check - observation date    
    if (~ml_training_dataset["ObservationPurchaseHealthTier"].isin(
        ["Healthy","Watch", "At Risk"]
    )).any():
        issues.append("Observation Purchase Health Tier check failed.")
    
    
    # Outcome Horizon
    calculated_outcome_dates = (
        ml_training_dataset["ObservationDate"]
        + timedelta(days=PREDICTION_HORIZON_DAYS)
    )
    
    if (calculated_outcome_dates > final_data_date).any():
        issues.append("Outcome horizon check failed.")
        
        
    #Observation date 7-day increment   
    observation_dates = (
        ml_training_dataset["ObservationDate"]
        .drop_duplicates()
        .sort_values()
    )
    
    observation_date_gaps = observation_dates.diff()
    
    if (
        observation_date_gaps.dropna() 
        != timedelta(days=OBSERVATION_FREQUENCY_DAYS)
    ).any():
        issues.append("Observation date increment check failed.")
    
    
    # Observation date validity
    observation_date_validity = pd.api.types.is_datetime64_any_dtype(
        ml_training_dataset["ObservationDate"]
    )
    
    if not observation_date_validity:
        issues.append("Observation date validity check failed.")


    # Target has both classes
    target_values = ml_training_dataset[
        "AtRiskOrCriticalWithin30Days"
    ].unique()
    
    if 0 not in target_values or 1 not in target_values:
        issues.append("Target is missing a class, check failed.")
    
    # Observation date is an actual date
    if ml_training_dataset["ObservationDate"].isna().any():
        issues.append("Missing observation date check failed.")
        
    passed = len(issues) == 0
    
    return {
            "name": "Training Target Labels",
            "passed": passed,
            "records_checked": len(ml_training_dataset),
            "issues_found": len(issues),
            "details": " | ".join(issues),
        }


def count_observation_dates_by_year(
    ml_training_dataset,
):
    
    observation_years = pd.to_datetime(
        ml_training_dataset["ObservationDate"]
    ).dt.year
    
    year_count = observation_years.value_counts().sort_index()
    
    return year_count
  
# ==========================================
# Main
# ==========================================

def main():

    ml_training_dataset = pd.read_csv(
        OUTPUT_DATA_PATH,
        parse_dates=["ObservationDate"],
    )

    observation_date_qa = validate_observation_dates()

    target_label_qa = validate_target_labels()

    training_target_labels = validate_training_target_labels(
        ml_training_dataset,
        TRAINING_FINAL_DATA_DATE,
    )
    
    observation_date_yearly_counts = count_observation_dates_by_year(
        ml_training_dataset,
    )
    
    print(observation_date_qa)
    print(target_label_qa)
    print(training_target_labels)
    print(observation_date_yearly_counts)


if __name__ == "__main__":
    main()