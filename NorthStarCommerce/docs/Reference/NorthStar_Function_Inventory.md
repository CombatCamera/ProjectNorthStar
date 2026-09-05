# NorthStar Commerce
## Function Inventory

Version 1.1

---

# Overview

This document provides a centralized inventory of the primary functions and configuration components used throughout NorthStar Commerce.

The inventory is organized by engine or module so that the location and responsibility of major project functions can be identified without inspecting every source file individually.

This document is intended as a navigation and maintenance reference. Detailed business logic remains defined by the Business Rules and implemented within the corresponding source modules.

---

# Generation Engine

**Module:** `generate_ecommerce_data.py`  
**Version:** 2.0

## Helper Functions

def round_currency(value):
def random_date(start: date, end: date) -> date:
def calculate_orders_for_year(
    join_date: date,
    shopping_profile: str,
    year: int,
    start_date: date,
    end_date: date,
) -> int:
def determine_shipping(loyalty_tier, subtotal):
def build_order_items_lookup(order_items):
def build_successful_payments_lookup(payments):
def generate_tracking_number(carrier):

## Customer Generation

def generate_customers(
    number_of_customers,
    start_date,
    end_date,
) -> list[dict]:

## Product Generation

def generate_categories() -> list[dict]:
def generate_products(
    categories: list[dict],
    end_date: date,
) -> list[dict]:

## Order Generation

def generate_orders(
    customers: list[dict],
    start_date: date,
    end_date: date,
) -> list[dict]:

def generate_order_items(orders, products):

def finalize_orders(
    orders,
    order_items_lookup,
    customer_lookup,
):

## Payment Generation

def generate_payments(orders):

## Shipping Generation

def generate_shipments(orders, payments):

## CSV Export

def write_csv(
    file_path: Path,
    records: list[dict],
    fieldnames: list[str],
) -> None:

## Main

def main() -> None:

# QA Engine

**Module:** `qa_validation.py`  
**Version:** 2.0

## Helper Functions

def round_currency(value):
def load_csv(file_path):
def build_order_items_lookup(order_items):
def build_order_id_counts(orders):
def get_duplicate_order_ids(order_id_counts):
def build_payments_lookup(payments):
def build_products_lookup(products):
def build_customers_lookup(customers):
def build_orders_lookup(orders):
def build_successful_payments_lookup(payments):

## Validation Functions

def validate_orders_have_items(orders, order_items):
def validate_unique_order_ids(orders):
def validate_orders_have_payments(orders, payments):
def validate_order_items_have_products(order_items, products):
def validate_orders_have_customers(orders, customers):
def validate_payments_have_orders(payments, orders):
def validate_payment_amounts_match_order_totals(orders, payments):
def validate_order_totals_reconciled(orders, order_items):
def validate_shipments_have_orders(shipments, orders):
def validate_shipments_have_successful_payments(shipments, payments):
def validate_shipment_dates_follow_payments(shipments, payments):
def validate_estimated_delivery_follows_shipment(shipments):
def validate_shipment_status_consistency(shipments):
def validate_delayed_shipments(shipments):
def validate_non_delayed_shipments_valid(shipments):
def validate_shipping_cost_match_orders(shipments, orders):
def validate_carrier_tracking_present(shipments):
def validate_shipment_status_values(shipments):

## Main

def main(
    customers_file,
    products_file,
    orders_file,
    order_items_file,
    payments_file,
    shipments_file=None
):

# Privacy Engine

**Module:** `privacy_engine.py`  
**Version:** 2.1.1

## Configuration

PROJECT_ROOT

PRIVACY_OUTPUT_FOLDER

def configure_dataset(dataset):

## Helper Functions

def load_csv(file_path):

def generate_anonymous_customer_mapping(customer_data):

def generate_anonymous_order_mapping(order_data):

def calculate_maximum_safe_offset(
    today,
    latest_event_date,
):

def generate_temporal_offset_mapping(
    customer_data,
    order_data,
    payment_data,
    anonymous_customer_map
):

def shift_datetime(date_string, temporal_offset_days):

def shift_date(date_string, temporal_offset_days):

## Privacy Transformation Functions

def filter_customer_data(
    customer_data,
    anonymous_customer_map,
    customer_temporal_offset_map
):

def filter_order_data(
    order_data,
    anonymous_customer_map,
    anonymous_order_map,
    customer_temporal_offset_map
):

def filter_payment_data(
    payment_data,
    anonymous_order_map,
    privacy_filtered_order_data,
    customer_temporal_offset_map
):

def reconstruct_purchase_history(
    privacy_filtered_customer_data,
    privacy_filtered_order_data,
    privacy_filtered_payment_data
):

## CSV Export

def write_csv(file_path, data, fieldnames):

## Main

def main(customer_file, order_file, payment_file):

# Privacy Engine QA

**Module:** `privacy_engine_qa.py`  
**Version:** 1.0

## Validation Functions

def validate_maximum_safe_offset():

## Main

def main():

# Feature Engineering Engine

**Module:** `feature_engineering.py`  
**Version:** 1.1

## Data Loading

def load_data(
    customers_file,
    orders_file,
    payments_file,
):

## Input Validation

def validate_required_columns(df, required_columns, dataset_name):
def validate_dataframe_not_empty(df, dataset_name):

def validate_inputs(
    customers_df,
    orders_df,
    payments_df,
    verbose=True,
):

## Helper Functions

def configure_dataset(dataset):
def round_currency(value):

## Output

def save_feature_dataset(feature_dataset, output_path):

## Business Data Preparation

def generate_successful_purchase_history(orders_df, payments_df):

def generate_purchase_history_as_of(
    successful_purchase_history,
    observation_date,
):

def generate_purchase_intervals(successful_purchase_history):

def generate_purchase_interval_changes(purchase_intervals):

## Temporal Features

def generate_temporal_features(
    successful_purchase_history,
    purchase_intervals,
    evaluation_date,
):

## Purchase Features

def generate_purchase_features(successful_purchase_history):

## Behavior Features

def meets_minimum_reliable_history(history):

def generate_purchase_interval_stddev(purchase_intervals):

def generate_average_interval_change(purchase_interval_changes):

def generate_behavior_features(
    purchase_intervals,
    purchase_interval_changes,
):

## Assembler

def assemble_feature_dataset(
    temporal_features,
    purchase_features,
    behavior_features,
):

## Feature Pipeline

def build_feature_dataset(
    observation_date=None,
    verbose=True,
):

## Main

def main():

# Feature QA Engine

**Module:** `feature_qa.py`  
**Version:** 1.0

## Feature Validation

def validate_purchase_interval_stddev():

def validate_average_interval_change():

def validate_purchase_frequency():

def validate_successful_purchase_history():

def validate_feature_dataset(
    feature_dataset,
    successful_purchase_history
):

## Historical Feature Validation

def validate_purchase_history_as_of():

def validate_historical_feature_dataset():

## Main

def main():

# Business Interpretation Engine

**Module:** `business_interpretation.py`  
**Version:** 1.0

## Business Interpretation

def generate_purchase_health(feature_dataset):

## Main

def main():

# Business Interpretation QA

**Module:** `business_interpretation_qa.py`  
**Version:** 1.0

## Business Interpretation Validation

def validate_purchase_health():

## Main

def main():

# Machine Learning Training Dataset Generator

**Module:** `ml_training_dataset_generator.py`  
**Version:** 2.0

## Helper Functions

def display_generation_progress(
    observation_number,
    total_observations,
    observation_date,
    start_time,
):

## Observation Generation

def generate_observation_dates(
    start_date,
    final_data_date,
):

def calculate_outcome_date(
    observation_date,
):

def generate_interpreted_snapshot(
    snapshot_date
):

def compare_purchase_health_snapshots(
    observation_snapshot,
    outcome_snapshot,
):

## Target Generation

def generate_target_label(
    purchase_health_comparison,
):

## Training Dataset Generation

def generate_training_observation(
    observation_date,
):

def generate_ml_training_dataset(
    observation_dates,
):

## Main

def main():

# ML Training Dataset QA Engine

**Module:** `ml_training_dataset_qa.py`  
**Version:** 1.0

## Validation Functions

def validate_observation_dates():

def validate_target_labels():

def validate_training_target_labels(
    ml_training_dataset,
    final_data_date,
):

## Diagnostic Functions

def count_observation_dates_by_year(
    ml_training_dataset,
):

## Main

def main():

# Machine Learning Engine

**Module:** `machine_learning_engine.py`  
**Version:** 1.0

## Temporal Dataset Preparation

def split_ml_training_dataset_by_time(
    ml_training_dataset
):

## Model Input Generation

def generate_X(
    dataset,
):

def generate_y(
    dataset,
):

## Prediction Generation

def generate_threshold_predictions(
    probabilities,
):

def generate_prediction_output(
    test_data,
    y_prob,
    y_threshold_pred,
):

## Model Training

def train_baseline_model(
    X_train,
    y_train,
):

## Main

def main():

# Machine Learning Engine QA

**Module:** `machine_learning_engine_qa.py`  
**Version:** 1.0

## Temporal Split Validation

def validate_training_prediction_horizon(
    training_data
):

def validate_embargo_period(
    embargo_data,
):

def validate_temporal_split_no_overlap(
    training_data,
    validation_embargo_data,
    validation_data,
    embargo_data,
    test_data,
):

def validate_dataframes_row_count(
    ml_training_dataset,
    training_data,
    embargo_data,
    test_data,
    validation_embargo_data,
    validation_data,
):

## Model Input Validation

def validate_X_y_row_counts(
    X_train,
    y_train,
):

def validate_X_y_indexes(
    X_train,
    y_train,
):

def validate_model_features(
    X_train,
):

def validate_target_column(
    y_train,
):

def validate_target_column_values(
    y_train,
):

def validate_X_train_values(
    X_train
):

## Prediction Validation

def validate_probability_row_count(
    X_test,
    y_prob,
):

def validate_prediction_row_count(
    X_test,
    y_threshold_pred,
):

def validate_prediction_values(
    y_threshold_pred,
):

def validate_probability_values(
    y_prob,
):

## Prediction Output Validation

def validate_output_columns(
    prediction_output,
):

def validate_output_row_count(
    prediction_output,
    test_data,
):

def validate_output_observation_alignment(
    prediction_output,
    test_data,
):

def validate_output_missing_values(
    prediction_output,
):

## Main

def main():

# Training Population Generator

**Module:** `generate_training_population.py`  
**Version:** 1.0

## Main

def main() -> None:

# Feature Pipeline Runner

**Module:** `run_feature_pipeline.py`  
**Version:** 1.0

## Main

def main():
