"""
=============================================================================
Project NorthStar - NorthStar Commerce
Machine Learning Engine
=============================================================================

Author: Mat Thompson
Created: 2026-08-28
Version: 1.0

Purpose:
Prepare certified historical training data for machine learning, train
predictive models, generate predictions, and evaluate model performance.

Primary Business Question:
Will this customer be At Risk or Critical 30 days from the observation date?

Responsibilities:
- Split historical observations into temporal training, validation, and testing datasets.
- Enforce embargo periods between training, validation, and testing.
- Separate approved model features from the prediction target.
- Train the baseline machine learning model.
- Generate probability and threshold predictions against unseen test data.
- Evaluate final model performance against unseen test outcomes.
- Generate and save the historical prediction output artifact.

Design Principles:
- Models learn from the past and are evaluated against the future.
- Future information must never enter model training features.
- Customer identifiers are retained for traceability but excluded as features.
- Model inputs must be explicitly approved before training.
- Prefer the simplest design that remains clear, maintainable, and teachable.

=============================================================================
"""

import pandas as pd

from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import (
    recall_score, 
    confusion_matrix,
    precision_score,
)

# ==========================================
# File Paths
# ==========================================

ML_TRAINING_FILE_PATH = (
    r"C:\Users\matth\Desktop\Data-Analytics-Portfolio\ProjectNorthStar\NorthStarCommerce\data\training\ml_training_dataset.csv"
)

# ==============================================
# Output Path
# ==============================================

PREDICTION_OUTPUT_FILE_PATH = (
    r"C:\Users\matth\Desktop\Data-Analytics-Portfolio\ProjectNorthStar"
    r"\NorthStarCommerce\data\predictions\customer_purchase_health_predictions.csv"
)

# ==========================================
# CONFIGURATION
# ==========================================

MODEL_FEATURES = [
    "DaysSinceLastPurchase",
    "AverageDaysBetweenPurchases",
    "SuccessfulOrderCount",
    "AverageOrderValue",
    "PurchaseFrequency",
    "PurchaseIntervalStdDev",
    "AverageIntervalChange",
    "HealthyWindowDays",
    "PercentBeyondHealthyWindow",
    "PurchaseHealthScore",
]

ALLOWED_MISSING_FEATURES = [
    "PurchaseIntervalStdDev",
    "AverageIntervalChange",
]

MODEL_DECISION_THRESHOLD = 0.325

# ==========================================
# Functions
# ==========================================

def split_ml_training_dataset_by_time(
    ml_training_dataset
):
    observation_dates = pd.to_datetime(
        ml_training_dataset["ObservationDate"]
    )
    
    test_start_date = pd.to_datetime(
       "2026-01-01"
    )
    training_cutoff_date = pd.to_datetime(
       "2025-12-01"
    )
    validation_start_date = pd.to_datetime(
       "2025-10-01"
    )
    validation_training_cutoff_date = pd.to_datetime(
       "2025-09-01"
    )
    
   
    training_mask = observation_dates <= validation_training_cutoff_date
   
    training_data = ml_training_dataset.loc[
        training_mask
    ].copy()


    test_mask = observation_dates >= test_start_date

    test_data = ml_training_dataset.loc[
        test_mask
    ].copy()


    embargo_mask = (
        (observation_dates > training_cutoff_date)
        & (observation_dates < test_start_date)
    )

    embargo_data = ml_training_dataset.loc[
        embargo_mask
    ].copy()


    validation_mask = (
        (observation_dates >= validation_start_date)
        & (observation_dates < training_cutoff_date)
    )
    
    validation_data = ml_training_dataset.loc[
        validation_mask
    ].copy()

    validation_embargo_mask = (
        (observation_dates > validation_training_cutoff_date)
        & (observation_dates < validation_start_date)
    )
    
    validation_embargo_data = ml_training_dataset.loc[
        validation_embargo_mask
    ].copy()
    

    return (
        training_data,
        validation_embargo_data,
        validation_data,
        embargo_data,
        test_data,
    )


def generate_X(
    dataset,
):
    
    X_train = dataset.loc[
        :,
        MODEL_FEATURES,
    ]
    
    return X_train


def generate_y(
    dataset,
):
    
    y_train = dataset.loc[
        :,
        
        "AtRiskOrCriticalWithin30Days",
        
    ]

    return y_train


def generate_threshold_predictions(
    probabilities,
):
    
    threshold_predictions = (
        probabilities >= MODEL_DECISION_THRESHOLD
    )
    
    return threshold_predictions


def generate_prediction_output(
    test_data,
    y_prob,
    y_threshold_pred,
):
    prediction_output = pd.DataFrame()
    
    prediction_output["AnonymousCustomerKey"] = (
        test_data["AnonymousCustomerKey"].values
    )

    prediction_output["ObservationDate"] = (
        test_data["ObservationDate"].values
    )
    
    prediction_output["AtRiskOrCriticalProbability"] = (
        y_prob
    )
    
    
    prediction_output["PredictedAtRiskOrCritical"] = (
        y_threshold_pred
    )
    
    return prediction_output


def train_baseline_model(
    X_train,
    y_train,
):
    
    baseline_model = HistGradientBoostingClassifier(
        random_state=42,
    )
    
    baseline_model.fit(
        X_train,
        y_train,
    )
    
    return baseline_model


# ==========================================
# Main
# ==========================================

def main():
    
    # Prepare Data
    ml_training_dataset = pd.read_csv(
        ML_TRAINING_FILE_PATH
    )
    
    (
        training_data,
        validation_embargo_data,
        validation_data,
        embargo_data,
        test_data,
    ) = split_ml_training_dataset_by_time(
        ml_training_dataset
    )
    
    
    # Training Inputs
    X_train = generate_X(training_data)
    
    y_train = generate_y(training_data)


    # Final Test Inputs
    X_test = generate_X(test_data)
        
    y_test = generate_y(test_data)
    

    # Machine Learning (Biff)
    
    # Train Model
    baseline_model = train_baseline_model(
        X_train,
        y_train,
    )
    
    
    # Generate final Test Predictions    
    y_prob = baseline_model.predict_proba(
        X_test,
    )[:, 1]
    
    y_threshold_pred = generate_threshold_predictions(
        y_prob,
    )
    
    # Generate Prediction Output
    prediction_output = generate_prediction_output(
        test_data,
        y_prob,
        y_threshold_pred,
    )

    # Save Prediction Output
    prediction_output.to_csv(
        PREDICTION_OUTPUT_FILE_PATH,
        index=False,
    )
    
    print("Prediction output saved successfully.")
    
    # Evaluate Final Test Performance   
    threshold_recall = recall_score(
        y_test,
        y_threshold_pred,
    )    
    
    threshold_precision = precision_score(
        y_test,
        y_threshold_pred,
    )
    
    threshold_confusion_matrix = confusion_matrix(
        y_test,
        y_threshold_pred,
    )
    
    
    print("Threshold Recall: ", threshold_recall)
    print("Threshold Precision: ", threshold_precision)
    print("Threshold Confusion Matrix:")
    print(threshold_confusion_matrix)
       
    
if __name__ == "__main__":
    main()