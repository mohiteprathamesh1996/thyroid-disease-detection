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
    TARGET_COLUMN
)
from thyroid.constant.training_pipeline import ARTIFACT_DIR
from thyroid.utils.main_utils import load_object


def main():
    try:
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)


if __name__ == "__main__":
    main()
