"""
THE 'mlflow.evaluation` MODULE IS LEGACY AND WILL BE REMOVED SOON. PLEASE DO NOT USE THESE CLASSES
IN NEW CODE. INSTEAD, USE `mlflow/entities/assessment.py` FOR ASSESSMENT CLASSES.
"""

import uuid
from typing import Optional

from mlflow.evaluation.evaluation import Evaluation, EvaluationEntity
from mlflow.evaluation.utils import evaluations_to_dataframes
from mlflow.tracking.client import MlflowClient
from mlflow.tracking.fluent import _get_or_start_run
from mlflow.utils.annotations import deprecated


@deprecated(since="3.0.0")
def log_evaluations(
    *, evaluations: list[Evaluation], run_id: Optional[str] = None
) -> list[EvaluationEntity]:
    """
    Logs one or more evaluations to an MLflow Run.

    Args:
      evaluations (List[Evaluation]): List of one or more MLflow Evaluation objects.
      run_id (Optional[str]): ID of the MLflow Run to log the evaluation. If unspecified, the
          current active run is used, or a new run is started.

    Returns:
      List[EvaluationEntity]: The logged Evaluation objects.
    """
    run_id = run_id if run_id is not None else _get_or_start_run().info.run_id
    if not evaluations:
        return []

    client = MlflowClient()
    evaluation_entities = [
        evaluation._to_entity(run_id=run_id, evaluation_id=uuid.uuid4().hex)
        for evaluation in evaluations
    ]
    evaluations_df, metrics_df, assessments_df, tags_df = evaluations_to_dataframes(
        evaluation_entities
    )
    client.log_table(run_id=run_id, data=evaluations_df, artifact_file="_evaluations.json")
    client.log_table(run_id=run_id, data=metrics_df, artifact_file="_metrics.json")
    client.log_table(run_id=run_id, data=assessments_df, artifact_file="_assessments.json")
    client.log_table(run_id=run_id, data=tags_df, artifact_file="_tags.json")

    return evaluation_entities
