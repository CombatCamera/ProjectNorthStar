# =============================================================================
# Project NorthStar - NorthStar Commerce
# Machine Learning Engine QA
# =============================================================================
#
# Author: Mat Thompson
# Created: 2026-08-28
# Version: 1.0
#
# Purpose:
# Validate the integrity of Machine Learning Engine inputs, temporal dataset
# separation, model predictions, and saved prediction outputs while protecting
# model training and evaluation from temporal and target leakage.
#
# Responsibilities:
# - Validate temporal training, validation, and testing boundaries.
# - Validate the 30-day prediction-horizon cutoff.
# - Validate embargo periods between temporal datasets.
# - Confirm temporal dataset observations do not improperly overlap.
# - Confirm approved model features and prediction targets are correctly separated.
# - Validate training and validation model inputs before model training.
# - Validate final prediction probabilities and threshold predictions.
# - Validate the saved historical prediction output artifact.
#
# QA Principle:
# The Machine Learning Engine must prove that Biff cannot see information
# from the future before Biff is allowed to learn.
#
# =============================================================================

import pandas as pd
from datetime import timedelta
from machine_learning.machine_learning_engine import (
    ML_TRAINING_FILE_PATH,
    MODEL_FEATURES,
    ALLOWED_MISSING_FEATURES,
    PREDICTION_OUTPUT_FILE_PATH,
    generate_threshold_predictions,
    train_baseline_model,
    split_ml_training_dataset_by_time,
    generate_X,
    generate_y,
)
# ==============================================
# Configuration
# ==============================================

PREDICTION_HORIZON_DAYS = 30
TEST_PERIOD_START = pd.to_datetime(
    "2026-01-01"
)
TRAINING_DATE_CUTOFF = pd.to_datetime(
    "2025-12-01"
)

# ==============================================
# Functions
# ==============================================

def validate_training_prediction_horizon(
    training_data
):
    
    issues = []
    
    observation_dates = pd.to_datetime(
        training_data["ObservationDate"]
    )
    
    outcome_dates = (
        observation_dates 
        + timedelta(days=PREDICTION_HORIZON_DAYS)
    )
    
    if (outcome_dates >= TEST_PERIOD_START).any():
        issues.append("Outcome dates check failed")
        
    return issues


def validate_embargo_period(
    embargo_data,
):
    
    issues = []
    
    observation_dates = pd.to_datetime(
        embargo_data["ObservationDate"]
    )
    
    if (observation_dates <= TRAINING_DATE_CUTOFF).any():
        issues.append("Embargo lower boundary check failed") 
        
    if (observation_dates >= TEST_PERIOD_START).any():
        issues.append("Embargo upper boundary check failed")
    
    return issues


def validate_temporal_split_no_overlap(
    training_data,
    validation_embargo_data,
    validation_data,
    embargo_data,
    test_data,
):
    
    issues = []
    
    training_observations = training_data.loc[
        :,
        [
            "AnonymousCustomerKey",
            "ObservationDate",
        ]
    ]
    
    embargo_observations = embargo_data.loc[
        :,
        [
            "AnonymousCustomerKey",
            "ObservationDate",
        ]
    ]
    
    test_observations = test_data.loc[
        :,
        [
            "AnonymousCustomerKey",
            "ObservationDate",
        ]
    ]
    
    validation_embargo_observations = validation_embargo_data.loc[
        :,
        [
            "AnonymousCustomerKey",
            "ObservationDate",
        ]
    ]

    validation_observations = validation_data.loc[
        :,
        [
            "AnonymousCustomerKey",
            "ObservationDate",
        ]
    ]
    
    training_embargo_overlap = training_observations.merge(
        embargo_observations,
        how="inner",
        on=[
            "AnonymousCustomerKey",
            "ObservationDate",
        ]
    )
    
    training_test_overlap = training_observations.merge(
        test_observations,
        how="inner",
        on=[
            "AnonymousCustomerKey",
            "ObservationDate",
        ]
    )
    
    training_validation_embargo_overlap = training_observations.merge(
        validation_embargo_observations,
        how="inner",
        on=[
            "AnonymousCustomerKey",
            "ObservationDate",
        ]
    )
    
    validation_embargo_validation_overlap = validation_embargo_observations.merge(
        validation_observations,
        how="inner",
        on=[
            "AnonymousCustomerKey",
            "ObservationDate",
        ]
    )
    
    validation_test_embargo_overlap = validation_observations.merge(
        embargo_observations,
        how="inner",
        on=[
            "AnonymousCustomerKey",
            "ObservationDate",
        ]
    )

    validation_test_overlap = validation_observations.merge(
    test_observations,
    how="inner",
    on=[
        "AnonymousCustomerKey",
        "ObservationDate",
    ]
)

    embargo_test_overlap = embargo_observations.merge(
        test_observations,
        how="inner",
        on=[
            "AnonymousCustomerKey",
            "ObservationDate",
        ]
    )   
       
    
    if(
        len(training_embargo_overlap) > 0
        or len(training_test_overlap) > 0
        or len(embargo_test_overlap) > 0
        or len(training_validation_embargo_overlap) > 0
        or len(validation_embargo_validation_overlap) > 0
        or len(validation_test_embargo_overlap) > 0
        or len(validation_test_overlap) > 0
    ):
        issues.append("Overlap check failed.")
        
    return issues


def validate_dataframes_row_count(
    ml_training_dataset,
    training_data,
    embargo_data,
    test_data,
    validation_embargo_data,
    validation_data,
):
    
    issues = []
    
    actual_dataset_rows = len(ml_training_dataset)
    
    training_rows = len(training_data)
    
    embargo_rows = len(embargo_data)
    
    test_rows = len(test_data)
    
    validation_embargo_rows = len(
        validation_embargo_data
    )
    
    validation_rows = len(
        validation_data
    )
    
    expected_dataset_rows = (
        training_rows
        + validation_embargo_rows
        + validation_rows
        + embargo_rows
        + test_rows
    )
    
    if expected_dataset_rows != actual_dataset_rows:
        issues.append("Row counts do not match.")
        
    return issues
    
    
def validate_X_y_row_counts(
    X_train,
    y_train,
):
    
    issues = []
    
    if len(X_train) != len(y_train):
        issues.append("Training counts do not match.")
        
    return issues


def validate_X_y_indexes(
    X_train,
    y_train,
):
    
    issues = []
    
    if not X_train.index.equals(y_train.index):
        issues.append("X and y indexes do not match.")
        
    return issues
        

def validate_model_features(
    X_train,
):
    
    issues = []
    
    if X_train.columns.tolist() != MODEL_FEATURES:
        issues.append("Model features check failed.")
        
    return issues


def validate_target_column(
    y_train,
):
    
    issues = []
    
    if y_train.name != "AtRiskOrCriticalWithin30Days":
        issues.append("Target column check failed.")
        
    return issues


def validate_target_column_values(
    y_train,
):
    issues = []
    
    if (~y_train.isin([0, 1])).any():
        issues.append("Invalid target column value detected.")
        
    return issues


def validate_X_train_values(
    X_train
):
    
    issues = []
    
    required_complete_features = []

    for column in X_train.columns:
        if column not in ALLOWED_MISSING_FEATURES:
            required_complete_features.append(column)
    
    if X_train.loc[
        :,
        required_complete_features,
    ].isna().any().any():
        issues.append("Missing value detected, check failed.")
    
    return issues


def validate_probability_row_count(
    X_test,
    y_prob,
):
    
    issues = []
    
    if len(X_test) != len(y_prob):
        issues.append("Probability row count check failed.")
    
    return issues


def validate_prediction_row_count(
    X_test,
    y_threshold_pred,
):
    
    issues = []
    
    if len(X_test) != len(y_threshold_pred):
        issues.append("Prediction row count check failed.")
        
    return issues


def validate_prediction_values(
    y_threshold_pred,
):
    
    issues = []
    
    if (~pd.Series(y_threshold_pred).isin([0, 1])).any():
        issues.append("Invalid prediction value detected.")
        
    return issues
    
    
def validate_probability_values(
    y_prob,
):
    
    issues = []
    
    if (
        (y_prob < 0.0).any()
        or (y_prob > 1.0).any()
    ):
        issues.append("Invalid probability value detected.")
        
    return issues
    
    
def validate_output_columns(
    prediction_output,
):
    
    issues = []
    
    expected_columns = [
        "AnonymousCustomerKey",
        "ObservationDate",
        "AtRiskOrCriticalProbability",
        "PredictedAtRiskOrCritical",
    ]
    
    actual_columns = prediction_output.columns.tolist()
    
    if actual_columns != expected_columns:
        issues.append("Prediction output columns check failed.")
        
    return issues
    
    
def validate_output_row_count(
    prediction_output,
    test_data,
):
    
    issues = []
    
    if len(prediction_output) != len(test_data):
        issues.append("Prediction output row count check failed.")
                      
    return issues
    
    
def validate_output_observation_alignment(
    prediction_output,
    test_data,
):
    
    issues = []
    
    output_observations = prediction_output.loc[
        :,
        [
            "AnonymousCustomerKey",
            "ObservationDate",
        ]
    ]
    
    test_observations = test_data.loc[
        :,
        [
            "AnonymousCustomerKey",
            "ObservationDate",
        ]
    ]
    
    output_observations["ObservationDate"] = pd.to_datetime(
        output_observations["ObservationDate"]
    )
    
    test_observations["ObservationDate"] = pd.to_datetime(
        test_observations["ObservationDate"]
    )
    
    output_observations = output_observations.reset_index(
        drop=True
    )
    
    test_observations = test_observations.reset_index(
        drop=True
    )
    
    sorted_output_observations = output_observations.sort_values(
        by=[
            "AnonymousCustomerKey",
            "ObservationDate",
        ]
    ).reset_index(
        drop=True
    )

    sorted_test_observations = test_observations.sort_values(
        by=[
            "AnonymousCustomerKey",
            "ObservationDate",
        ]
    ).reset_index(
        drop=True
    )
    
    if sorted_output_observations.equals(sorted_test_observations) == False:
        issues.append("Prediction output observation alignment check failed.")
    
    return issues


def validate_output_missing_values(
    prediction_output,
):
    
    issues = []
    
    if prediction_output.isna().any().any() == True:
        issues.append("Prediction output missing value check failed.")
        
    return issues


# ==============================================
# main
# ==============================================

def main():
    
    # Prepare Data
    ml_training_dataset = pd.read_csv(
            ML_TRAINING_FILE_PATH
        )
    
    prediction_output = pd.read_csv(
        PREDICTION_OUTPUT_FILE_PATH
    )
    
    (
        training_data,
        validation_embargo_data,
        validation_data,
        embargo_data,
        test_data,
    ) = split_ml_training_dataset_by_time(
        ml_training_dataset,
    )  
    
    
    X_train = generate_X(
        training_data
    )
        
    y_train = generate_y(
        training_data
    )
    
    X_test = generate_X(
        test_data
    )
    
    X_validation = generate_X(
        validation_data
    )
    
    y_validation = generate_y(
        validation_data
    )
    
    
    
    # Temporal Split QA
    prediction_horizon_issues = (
        validate_training_prediction_horizon(training_data)
    )
    
    embargo_issues = (
        validate_embargo_period(embargo_data)
    )
    
    overlap_issues = validate_temporal_split_no_overlap(
        training_data,
        validation_embargo_data,
        validation_data,
        embargo_data,
        test_data,
    )
    
    dataframe_row_count_issues = validate_dataframes_row_count(
        ml_training_dataset,
        training_data,
        validation_embargo_data,
        validation_data,
        embargo_data,
        test_data,
    )
    
    
    
    # Training Input QA
    training_input_row_count_issues = validate_X_y_row_counts(
        X_train,
        y_train,
    )
    
    training_index_issues = validate_X_y_indexes(
        X_train,
        y_train
    )
    
    training_model_feature_issues = validate_model_features(
        X_train
    )
    
    training_target_column_issues = validate_target_column(
        y_train
    )
    
    training_target_value_issues = validate_target_column_values(
        y_train
    )
    
    training_feature_value_issues = validate_X_train_values(
        X_train
    )
    
    
    
    # Validation Input QA
    validation_input_row_count_issues = validate_X_y_row_counts(
        X_validation,
        y_validation,
    )
    
    validation_index_issues = validate_X_y_indexes(
        X_validation,
        y_validation,
    )
    
    validation_model_feature_issues = validate_model_features(
        X_validation,
    )
    
    validation_target_column_issues = validate_target_column(
        y_validation,
    )    
    
    validation_target_value_issues = validate_target_column_values(
        y_validation
    )
    
    validation_feature_value_issues = validate_X_train_values(
        X_validation
    )
    
    
    
    # Final Prediction QA
    baseline_model = train_baseline_model(
        X_train,
        y_train,
    )
    
    y_prob = baseline_model.predict_proba(
        X_test
    )[:, 1]
    
    y_threshold_pred = generate_threshold_predictions(
        y_prob,
    )
    
    prediction_row_count_issues = validate_prediction_row_count(
        X_test,
        y_threshold_pred,
    )  
    
    prediction_value_issues = validate_prediction_values(
        y_threshold_pred,
    )
    
    probability_value_issues = validate_probability_values(
        y_prob,
    )
    
    probability_row_count_issues = validate_probability_row_count(
        X_test,
        y_prob,
    )
    
    
    # Prediction Output File QA
    output_column_issues = validate_output_columns(
        prediction_output,
    )
    
    output_row_count_issues = validate_output_row_count(
        prediction_output,
        test_data,
    )
    
    output_observation_alignment_issues = validate_output_observation_alignment(
        prediction_output,
        test_data,
    )
    
    output_probability_issues = validate_probability_values(
        prediction_output["AtRiskOrCriticalProbability"]
    )
    
    output_prediction_value_issues = validate_prediction_values(
        prediction_output["PredictedAtRiskOrCritical"]
    )
    
    output_missing_value_issues = validate_output_missing_values(
        prediction_output,
    )
    
    
    
    
    # QA Results
    temporal_split_issues = (
        prediction_horizon_issues
        + embargo_issues
        + overlap_issues
        + dataframe_row_count_issues
    )
    
    training_input_issues = (
        training_input_row_count_issues
        + training_index_issues
        + training_model_feature_issues
        + training_target_column_issues
        + training_target_value_issues
        + training_feature_value_issues
    )
    
    validation_input_issues = (
        validation_input_row_count_issues
        + validation_index_issues
        + validation_model_feature_issues
        + validation_target_column_issues
        + validation_target_value_issues
        + validation_feature_value_issues
    )
    
    final_prediction_issues = (
        prediction_row_count_issues
        + prediction_value_issues
        + probability_value_issues
        + probability_row_count_issues
    )
    
    prediction_output_file_issues = (
        output_column_issues
        + output_row_count_issues
        + output_observation_alignment_issues
        + output_probability_issues
        + output_prediction_value_issues
        + output_missing_value_issues
    )
    
    all_issues = (
        temporal_split_issues
        + training_input_issues
        + validation_input_issues
        + final_prediction_issues
        + prediction_output_file_issues
    )
    
    if len(all_issues) > 0:
        print("Machine Learning Engine QA: FAILED")
        
        for issue in all_issues:   
            print(issue)
    else:
        print("Machine Learning Engine QA: PASSED")
        
    
if __name__ == "__main__":
    main()