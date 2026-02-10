from src.pipeline.models.dag_docker_task_config_model import DagDockerTaskModel
from src.pipeline.models.dag_etl_build_model import DagETLBuildModel
from src.pipeline.models.dag_materialize_build_model import DagMaterializeBuildModel
from src.pipeline.models.dag_stream_build_model import DagStreamBuildModel


class EADagBuildConfigs:
    EA_ETL_DAG_BUILD_CONFIGS = DagETLBuildModel(
        ingest_task=DagDockerTaskModel(
            task_id="ea_ingest_task",
        ),
        clean_task=DagDockerTaskModel(
            task_id="ea_clean_task",
        ),
        explore_and_validate_task=DagDockerTaskModel(
            task_id="ea_explore_and_validate_task",
        )
    )
    
    EA_STREAM_DAG_BUILD_CONFIGS = DagStreamBuildModel(
        stream_to_online_task=DagDockerTaskModel(
            task_id="ea_stream_to_online_task",
        ),
        stream_to_offline_task=DagDockerTaskModel(
            task_id="ea_stream_to_offline_task",
        )
    )
    
    EA_MATERIALIZE_DAG_BUILD_CONFIGS = DagMaterializeBuildModel(
        materialize_task=DagDockerTaskModel(
            task_id="ea_materialize_task",
        )
    )
    
    
    
    
    
    