import os
from sklearn.model_selection import train_test_split
import polars as pl
# Import our custom modules
import data_processing
import model
from config_reader import ConfigReader

config = ConfigReader("configs/config.yaml").config

def run_training_pipeline():
    """Executes the full model training pipeline."""
    print("--- Starting Model Training Pipeline ---")

    # 1. Data Processing and Feature Engineering
    raw_df = pl.read_csv(r"data/datav1.csv")
    processed_df = data_processing.engineer_features(raw_df)

    # 2. Data Splitting
    X = processed_df[config["features"]]
    y = processed_df[config['target']]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config['test_size'], random_state=config['random_state']
    )
    print(f"Data split into training ({len(X_train)} samples) and testing ({len(X_test)} samples).")

    # 3. Model Training
    trained_model = model.train_model(X_train, y_train, config['model_params'])

    # 4. Model Evaluation
    model.evaluate_model(trained_model, X_test, y_test)

    # 5. Model Saving
    # Ensure the 'models' directory exists
    os.makedirs(os.path.dirname(config['model_name']), exist_ok=True)
    model.save_model(trained_model, config['model_name'])

    print("--- Model Training Pipeline Finished Successfully! 🎉 ---")


if __name__ == "__main__":
    run_training_pipeline()