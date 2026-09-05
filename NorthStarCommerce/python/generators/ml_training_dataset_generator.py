
"""
===============================================================================
Project NorthStar
Machine Learning Training Dataset Generator
-------------------------------------------------------------------------------
Author: Mat Thompson
Created: 2026-08-11
Last Updated: 2026-08-27
Version: 2.0

Purpose:
Generate historical machine learning training observations from NorthStar's
privacy-filtered customer behavior data.

Business Objective:
Create point-in-time training records that allow machine learning models to
learn whether a customer's purchase health is likely to deteriorate within a
defined prediction horizon.

Core Responsibilities:
- Generate historical observation dates.
- Reconstruct customer features as they existed at each observation date.
- Apply NorthStar's canonical Business Interpretation Engine.
- Establish customer purchase health at the observation date.
- Evaluate customer purchase health at the prediction outcome date.
- Generate supervised machine learning target labels.
- Prevent future information from leaking into historical feature records.
- Produce a reusable ML training dataset for downstream model development.

Training Flow:
Historical Data
    -> Observation Date
    -> Point-in-Time Feature Dataset
    -> Business Interpretation
    -> Observation Purchase Health
    -> Prediction Horizon
    -> Outcome Purchase Health
    -> Target Label
    -> ML Training Record

Prediction Target:
AtRiskOrCriticalWithin30Days

Engineering Principles:
- Feature Engineering creates evidence.
- Business Interpretation determines what the evidence means.
- Machine learning learns to anticipate future business outcomes.
- Business truth must be defined independently of machine learning.
- Training features must contain only information available at observation time.
- Future information may determine the target label but must never leak into
  observation features.
- QA must validate training logic before datasets are approved for model use.
- Prefer the simplest design that remains clear, maintainable, and teachable.

Machine Learning Principle:
One engine creates the business truth.
The second engine learns to anticipate it.

Version 2.0 Scope:
30-Day Customer Purchase Health Risk Prediction
===============================================================================
"""
from pathlib import Path
from datetime import timedelta
from time import perf_counter
import pandas as pd

from generators.feature_engineering import (
    build_feature_dataset,
)

from Interpretation.business_interpretation import (
    generate_purchase_health,
)


# =================================================
# CONFIGURATION
# =================================================

PREDICTION_HORIZON_DAYS = 30

OBSERVATION_FREQUENCY_DAYS = 7

TRAINING_OBSERVATION_START_DATE = pd.to_datetime("2023-01-01")

TRAINING_FINAL_DATA_DATE = pd.to_datetime("2026-08-18")

# =================================================
# Output Path
# =================================================

OUTPUT_DATA_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "training"
    / "ml_training_dataset.csv"
)

# =================================================
# Helper Functions
# =================================================

def display_generation_progress(
    observation_number,
    total_observations,
    observation_date,
    start_time,
):
    
    elapsed_time = perf_counter() - start_time
    
    average_time_per_observation = (
        elapsed_time
        / observation_number
    )
    
    remaining_observations = (
        total_observations 
        - observation_number
    )
    
    estimated_remaining_time = (
        average_time_per_observation
        * remaining_observations
    )
    
    elapsed_minutes, elapsed_seconds = divmod(
        int(elapsed_time),
        60,
    )
    
    eta_minutes, eta_seconds = divmod(
        int(estimated_remaining_time),
        60,
    )
    
    percent_complete = (
        observation_number
        / total_observations
        * 100
    )
    
    bar_width = 20
    
    filled_width = int(
        bar_width * percent_complete / 100
    )
    
    progress_bar = (
        "█" * filled_width
        + "░" * (bar_width - filled_width)
    )

    print(
    f"\r[{progress_bar}] "
    f"{percent_complete:5.1f}% | "
    f"{observation_number}/{total_observations} | "
    f"{observation_date:%Y-%m-%d} | "
    f"{elapsed_minutes:02d}:{elapsed_seconds:02d} | "
    f"ETA {eta_minutes:02d}:{eta_seconds:02d}",
    end="",
    flush=True,
)
      
# =================================================
# FUNCTIONS
# =================================================

def generate_observation_dates(
    start_date,
    final_data_date,
):
    
    last_valid_observation_date = (
        final_data_date
        - timedelta(days=PREDICTION_HORIZON_DAYS)
    )
    
    observation_dates = pd.date_range(
        start=start_date,
        end=last_valid_observation_date,
        freq=f"{OBSERVATION_FREQUENCY_DAYS}D"
    )   
    
    return observation_dates


def calculate_outcome_date(
    observation_date,
):
    
    outcome_date = (
        observation_date 
        + timedelta(days=PREDICTION_HORIZON_DAYS)
    )

    return outcome_date


def generate_interpreted_snapshot(
    snapshot_date
):
    
    feature_dataset, _ = build_feature_dataset(
        snapshot_date,
        verbose=False,
    )

    purchase_health = generate_purchase_health(
        feature_dataset
    )

    return purchase_health


def compare_purchase_health_snapshots(
    observation_snapshot,
    outcome_snapshot,
):

    observation_snapshot = observation_snapshot.rename(
        columns={
            "PurchaseHealthTier": "ObservationPurchaseHealthTier"
        }
    )

    outcome_snapshot = outcome_snapshot.rename(
        columns={
            "PurchaseHealthTier": "OutcomePurchaseHealthTier"
        }
    )

    outcome_snapshot = outcome_snapshot[
        [
            "AnonymousCustomerKey",
            "OutcomePurchaseHealthTier",
        ]
    ].copy()

    purchase_health = pd.merge(
        observation_snapshot,
        outcome_snapshot,
        on="AnonymousCustomerKey",
        how="inner",
    )

    return purchase_health


def generate_target_label(
    purchase_health_comparison,
):
    
    eligible_training_records = purchase_health_comparison.loc[
        purchase_health_comparison[
            "ObservationPurchaseHealthTier"
        ].isin(
            [
                "Healthy",
                "Watch",
                "At Risk",
            ]
        )
    ].copy()
    
    eligible_training_records["AtRiskOrCriticalWithin30Days"] = 0
    
    positive_outcomes = eligible_training_records[
        "OutcomePurchaseHealthTier"
    ].isin(
        [
            "At Risk",
            "Critical",
        ]
    )

    eligible_training_records.loc[
        positive_outcomes,
        "AtRiskOrCriticalWithin30Days"
    ] = 1
    
    return eligible_training_records


def generate_training_observation(
    observation_date,
):
    
    outcome_date = calculate_outcome_date(
        observation_date
    )
    
    observation_snapshot = generate_interpreted_snapshot(
        observation_date
    )
    
    outcome_snapshot = generate_interpreted_snapshot(
        outcome_date
    )
    
    purchase_health_comparison = compare_purchase_health_snapshots(
        observation_snapshot,
        outcome_snapshot,
    )
    
    training_records = generate_target_label(
        purchase_health_comparison
    )
    
    training_records["ObservationDate"] = observation_date
    
    return training_records
    
    
def generate_ml_training_dataset(
    observation_dates,
):
   
    start_time = perf_counter()
    
    training_batches = []
    total_observation = len(observation_dates)
    
    
    for observation_number, observation_date in enumerate(
        observation_dates,
        start=1,
    ):
        training_records = generate_training_observation(
            observation_date
        )
        
        training_batches.append(
            training_records
        )

        display_generation_progress(
            observation_number,
            total_observation,
            observation_date,
            start_time,
        )
        
    print()
    
    ml_training_dataset = pd.concat(
        training_batches,
        ignore_index=True,
    )
    
    return ml_training_dataset

# =================================================
# MAIN
# =================================================

def main():

    observation_dates = generate_observation_dates(
        TRAINING_OBSERVATION_START_DATE,
        TRAINING_FINAL_DATA_DATE,
    )

    ml_training_dataset = generate_ml_training_dataset(
        observation_dates
    )

    # Ensure output directory exists
    OUTPUT_DATA_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Save file
    ml_training_dataset.to_csv(
        OUTPUT_DATA_PATH,
        index=False,
    )


if __name__ == "__main__":
    main()