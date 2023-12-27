import io
import os
import numpy as np
import pandas as pd
from fastapi import FastAPI, UploadFile, File
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

from thyroid.logger import logging
from thyroid.pipeline.training_pipeline import TrainPipeline
from thyroid.constant.training_pipeline import (
    DATA_INGESTION_DIR_NAME,
    DATA_INGESTION_INGESTED_DIR,
    TRAIN_FILE_NAME,
    SAVED_MODEL_DIR,
    TARGET_COLUMN,
    SCHEMA_FILE_PATH
)
from thyroid.constant.training_pipeline import ARTIFACT_DIR
from thyroid.constant.application import APP_HOST, APP_PORT
from thyroid.ml.model.estimator import ModelResolver
from thyroid.utils.main_utils import load_object, read_yaml_file

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try:

        train_pipeline = TrainPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")


@app.post("/predict")
async def predict_route(file: UploadFile = File(...)):
    try:
        contents = await file.read()  # Read the contents of the uploaded file
        # Use io.BytesIO to read bytes as CSV
        df = pd.read_csv(io.BytesIO(contents))
        # Process the DataFrame (e.g., perform operations, save to disk, etc.)
        directory = ARTIFACT_DIR
        files_with_timestamps = [
            (
                filename,
                os.path.getctime(os.path.join(directory, filename))
            )
            for filename in os.listdir(directory)
        ]

        latest_file = max(files_with_timestamps, key=lambda x: x[1])[
            0] if files_with_timestamps else None

        latest_file_path_csv = os.path.join(
            directory,
            latest_file,
            DATA_INGESTION_DIR_NAME,
            DATA_INGESTION_INGESTED_DIR,
            TRAIN_FILE_NAME
        )

        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)

        if not model_resolver.is_model_exists():
            return Response("Model is not available")

        config_schema = read_yaml_file(file_path=SCHEMA_FILE_PATH)

        str_cols = [
            list(i.keys())[0] for i in config_schema["columns"]
            if i[list(i.keys())[0]] == "object"
        ]

        str_cols.remove(TARGET_COLUMN)

        best_model_path = model_resolver.get_best_model_path()

        model = load_object(file_path=best_model_path)

        y_pred = model.predict(
            pd.get_dummies(
                data=df.replace("?", np.nan),
                columns=str_cols
            )[
                list(
                    model.preprocessor.feature_names_in_
                )
            ]
        )

    except Exception as e:
        return Response(f"Error Occurred! {e}")

    return {"predictions": y_pred.tolist()}


def main():
    try:
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)


if __name__ == "__main__":
    main()
    app_run(app, host=APP_HOST, port=APP_PORT)
