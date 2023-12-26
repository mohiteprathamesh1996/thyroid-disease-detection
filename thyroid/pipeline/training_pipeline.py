from thyroid.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig, 
    DataValidationConfig,
    DataTransformationConfig
)


from thyroid.exception import ThyroidException
from thyroid.logger import logging

from thyroid.entity.artifact_entity import (
    DataIngestionArtifact, 
    DataValidationArtifact,
    DataTransformationArtifact
)

from thyroid.component.data_ingestion import DataIngestion
from thyroid.component.data_validation import DataValidation
from thyroid.component.data_transformation import DataTransformation

import os
import sys


class TrainPipeline:
    is_pipeline_running = False

    def __init__(self):
        training_pipeline_config = TrainingPipelineConfig()
        self.training_pipeline_config = training_pipeline_config

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            self.data_ingestion_config = DataIngestionConfig(
                training_pipeline_config=self.training_pipeline_config
            )
            logging.info("Starting data ingestion")
            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(
                f"Data ingestion completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise ThyroidException(e, sys)
        
    def start_data_validation(
        self, 
        data_ingestion_artifact:DataIngestionArtifact
        )->DataValidationArtifact:
        try:
            self.data_validation_config = DataValidationConfig(
                training_pipeline_config=self.training_pipeline_config
                )
            data_validation = DataValidation(
                data_ingestion_artifact = data_ingestion_artifact,
                data_validation_config = self.data_validation_config
                )
            
            data_validation_artifact = data_validation.initiate_data_validation()
            return data_validation_artifact
        
        except Exception as e:
            raise ThyroidException(e, sys)

    def start_data_transformation(
            self,
            data_validation_artifact:DataValidationArtifact
            ):
        try:
            self.data_transformation_config = DataTransformationConfig(
                training_pipeline_config=self.training_pipeline_config
                )  
            
            data_transformation = DataTransformation(
                data_validation_artifact=data_validation_artifact, 
                data_transformation_config=self.data_transformation_config
                )
            
            data_transformation_artifact = data_transformation.initiate_data_transformation()

            return data_transformation_artifact      
            
        except Exception as e:
            raise ThyroidException(e, sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact
                )
            
            data_transformation_artifact = self.start_data_transformation(
                data_validation_artifact=data_validation_artifact
                )

        except Exception as e:
            raise ThyroidException(e, sys)