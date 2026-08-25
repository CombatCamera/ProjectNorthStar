from generators.feature_engineering import (
    build_feature_dataset,
    save_feature_dataset,
)
from utilities.feature_qa import validate_feature_dataset

# =============================================================================
# CONFIGURATION
# =============================================================================

OUTPUT_PATH = r"C:\Users\matth\Desktop\Data-Analytics-Portfolio\ProjectNorthStar\NorthStarCommerce\data\training_dataset\customer_behavior_features.csv"

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
            "Feature Dataset QA did not pass. Output file was not created."
        )
        
        
    save_feature_dataset(
        feature_dataset,
        OUTPUT_PATH,
    )
    print(f"✓ Feature dataset saved: {OUTPUT_PATH}")
    
if __name__ == "__main__":
    main()