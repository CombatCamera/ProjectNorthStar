"""
===============================================================================
Project NorthStar
Feature Pipeline Runner
-------------------------------------------------------------------------------
Author: Mat Thompson
Created: 2026-08-25
Last Updated: 2026-08-30
Version: 1.0

Purpose:
Orchestrate the Feature Engineering pipeline from feature generation through
final QA certification and approved output generation.

Business Objective:
Ensure that NorthStar feature datasets are generated, validated, and written
to disk only after successfully passing the required quality checks.

Core Responsibilities:
- Trigger Feature Engineering dataset generation.
- Receive the assembled feature dataset and supporting business history.
- Run final Feature Dataset QA certification.
- Enforce fail-closed output behavior.
- Prevent uncertified feature datasets from being written.
- Write the certified feature dataset to the configured output location.
- Provide clear success and failure reporting.

Pipeline Flow:
Build Feature Dataset
        ↓
Feature Dataset QA
        ↓
QA Passed?
   ├── No  → Block Output
   └── Yes → Save Certified Dataset

Fail-Closed Policy:
If Feature Dataset QA does not pass, the output file must not be created or
overwritten.

Output:
customer_behavior_features.csv

Engineering Principles:
- Orchestration coordinates; specialist modules perform the work.
- Feature Engineering generates business evidence.
- Feature QA certifies business evidence.
- Output generation occurs only after QA approval.
- Failed QA must block downstream output.
- Keep the runner simple, readable, and free of feature-generation logic.

Future Expansion:
This runner may later coordinate additional Feature Engineering modes,
historical observation pipelines, expanded Feature QA certification,
and logging while remaining within the Feature Engineering layer.
===============================================================================
"""

from generators.feature_engineering import (
    build_feature_dataset,
    save_feature_dataset,
)
from utilities.feature_qa import validate_feature_dataset

# =============================================================================
# CONFIGURATION
# =============================================================================

OUTPUT_PATH = (
    r"C:\Users\matth\Desktop\Data-Analytics-Portfolio\ProjectNorthStar\NorthStarCommerce\data\training_dataset\customer_behavior_features.csv"
)

# =============================================================================
# MAIN
# =============================================================================

def main():
    
    feature_dataset, successful_purchase_history = build_feature_dataset()

    qa_result = validate_feature_dataset(
        feature_dataset,
        successful_purchase_history,
    )
    
    if not qa_result["passed"]:
        raise RuntimeError(
            "Feature Dataset QA did not pass. "
            f"{qa_result['details']} "
            "Output file was not created."
        )
         
    save_feature_dataset(
        feature_dataset,
        OUTPUT_PATH,
    )
    print(f"✓ Feature dataset saved: {OUTPUT_PATH}")
    
if __name__ == "__main__":
    main()