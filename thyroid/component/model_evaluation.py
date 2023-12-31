from thyroid.exception import ThyroidException
from thyroid.logger import logging

from thyroid.entity.artifact_entity import (
    DataValidationArtifact,
    ModelTrainerArtifact,
    ModelEvaluationArtifact
)

from thyroid.entity.config_entity import ModelEvaluationConfig
import sys
from thyroid.ml.metric.classification_metric import get_classification_score
from thyroid.ml.model.estimator import ThyroidModel
from thyroid.utils.main_utils import (
    load_object,
    write_yaml_file,
    read_yaml_file
)

from thyroid.ml.model.estimator import ModelResolver
from thyroid.constant.training_pipeline import TARGET_COLUMN, SCHEMA_FILE_PATH
from thyroid.ml.model.estimator import TargetValueMapping
import pandas as pd
import numpy as np


class ModelEvaluation:
    def __init__(
            self,
            model_eval_config: ModelEvaluationConfig,
            data_validation_artifact: DataValidationArtifact,
            model_trainer_artifact: ModelTrainerArtifact
    ):

        try:
            self.model_eval_config = model_eval_config
            self.data_validation_artifact = data_validation_artifact
            self.model_trainer_artifact = model_trainer_artifact

        except Exception as e:
            raise ThyroidException(e, sys)

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            valid_train_file_path = self.data_validation_artifact.valid_train_file_path
            valid_test_file_path = self.data_validation_artifact.valid_test_file_path

            # valid train and test file dataframe
            train_df = pd.read_csv(valid_train_file_path)
            test_df = pd.read_csv(valid_test_file_path)

            df = pd.concat([train_df, test_df])
            y_true = df[TARGET_COLUMN]
            y_true.replace(TargetValueMapping().to_dict(), inplace=True)
            df.drop(TARGET_COLUMN, axis=1, inplace=True)

            train_model_file_path = self.model_trainer_artifact.trained_model_file_path
            model_resolver = ModelResolver()
            is_model_accepted = True

            if not model_resolver.is_model_exists():
                model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=is_model_accepted,
                    improved_accuracy=None,
                    best_model_path=None,
                    trained_model_path=train_model_file_path,
                    train_model_metric_artifact=self.model_trainer_artifact.test_metric_artifact,
                    best_model_metric_artifact=None
                )

                logging.info(
                    f"Model evaluation artifact: {model_evaluation_artifact}")

                return model_evaluation_artifact

            latest_model_path = model_resolver.get_best_model_path()
            latest_model = load_object(file_path=latest_model_path)
            train_model = load_object(file_path=train_model_file_path)

            config_schema = read_yaml_file(file_path=SCHEMA_FILE_PATH)

            str_cols = [
                list(i.keys())[0] for i in config_schema["columns"]
                if i[list(i.keys())[0]] == "object"
            ]

            str_cols.remove(TARGET_COLUMN)

            y_trained_pred = train_model.predict(
                pd.get_dummies(
                    data=df.replace("?", np.nan),
                    columns=str_cols
                )[list(train_model.preprocessor.feature_names_in_)]
            )

            y_latest_pred = latest_model.predict(
                pd.get_dummies(
                    data=df.replace("?", np.nan),
                    columns=str_cols
                )[list(train_model.preprocessor.feature_names_in_)]
            )

            trained_metric = get_classification_score(y_true, y_trained_pred)
            latest_metric = get_classification_score(y_true, y_latest_pred)

            improved_accuracy = trained_metric.f1_score - latest_metric.f1_score

            if self.model_eval_config.change_threshold < improved_accuracy:
                # 0.02 < 0.03
                is_model_accepted = True
            else:
                is_model_accepted = False

            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=is_model_accepted,
                improved_accuracy=improved_accuracy,
                best_model_path=latest_model_path,
                trained_model_path=train_model_file_path,
                train_model_metric_artifact=trained_metric,
                best_model_metric_artifact=latest_metric
            )

            model_eval_report = model_evaluation_artifact.__dict__

            # save the report
            write_yaml_file(
                self.model_eval_config.report_file_path, model_eval_report)
            logging.info(
                f"Model evaluation artifact: {model_evaluation_artifact}")

            return model_evaluation_artifact

        except Exception as e:
            raise ThyroidException(e, sys)
