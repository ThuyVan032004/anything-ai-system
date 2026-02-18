# import os

from shared.src.common.env_constants import EnvConstants
from shared.src.pipeline.models.dag_docker_task_config_model import DagDockerTaskModel
from shared.src.pipeline.models.dag_etl_build_model import DagETLBuildModel

from airflow.models import Variable

AWS_S3_BUCKET = Variable.get("AWS_S3_BUCKET")
AWS_ACCESS_KEY_ID = Variable.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = Variable.get("AWS_SECRET_ACCESS_KEY")

print(f"AWS_S3_BUCKET: {AWS_S3_BUCKET}")
print(f"AWS_ACCESS_KEY_ID: {AWS_ACCESS_KEY_ID}")
print(f"AWS_SECRET_ACCESS_KEY: {AWS_SECRET_ACCESS_KEY}")


class EADagBuildConfigs:
    EA_ETL_DAG_BUILD_CONFIGS = DagETLBuildModel(
        # ingest_task=DagDockerTaskModel(
        #     task_id="ea_ingest_task",
        # ),
        clean_task=DagDockerTaskModel(
            task_id="ea_clean_task",
            image="emotion_analysis/data_pipelines:latest",
            command="/bin/bash -c 'python -m emotion_analysis.data.ea_data_cleaning'",
            environment={
                "AWS_S3_BUCKET": AWS_S3_BUCKET,
                "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
                "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
            }
        ),
        explore_and_validate_task=DagDockerTaskModel(
            task_id="ea_explore_and_validate_task",
            image="emotion_analysis/data_pipelines:latest",
            command="/bin/bash -c 'python -m emotion_analysis.data.ea_data_profiling'",
            environment={
                "AWS_S3_BUCKET": AWS_S3_BUCKET,
                "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
                "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
            }
        )
    )
    
    # EA_STREAM_DAG_BUILD_CONFIGS = DagStreamBuildModel(
    #     stream_to_online_task=DagDockerTaskModel(
    #         task_id="ea_stream_to_online_task",
    #     ),
    #     stream_to_offline_task=DagDockerTaskModel(
    #         task_id="ea_stream_to_offline_task",
    #     )
    # )
    
    # EA_MATERIALIZE_DAG_BUILD_CONFIGS = DagMaterializeBuildModel(
    #     materialize_task=DagDockerTaskModel(
    #         task_id="ea_materialize_task",
    #     )
    # )
    
    
    
    
    
    