import os

# Define common constant variables for training pipeline
TARGET_COLUMN = "class"
PIPELINE_NAME = "thyroid"
ARTIFACT_DIR = "artifact"
FILE_NAME = "thyroid.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"
SAVED_MODEL_DIR = os.path.join("saved_models")
MODEL_FILE_NAME = "model.pkl"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")
SCHEMA_DROP_COLS = "drop_columns"

# Define constants for data ingestion
DATA_INGESTION_COLLECTION_NAME = "thyroid"
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR = "feature_store"
DATA_INGESTION_INGESTED_DIR = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2

