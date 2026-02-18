from shared.src.pipeline.etl_dag_base import ETLDagBase
from shared.src.pipeline.models.dag_config_model import DagConfigModel
from shared.src.pipeline.models.dag_etl_build_model import DagETLBuildModel

from emotion_analysis.pipelines.configs.ea_dag_build_configs import EADagBuildConfigs


class EAETLDag(ETLDagBase):
    def __init__(self, configs: DagConfigModel):
        super().__init__(configs)
        
    def build(self, build_configs: DagETLBuildModel):
        return super().build(build_configs)
    

ea_etl_dag_configs = DagConfigModel(
    dag_id="ea_etl_dag"
)

ea_etl_dag = EAETLDag(ea_etl_dag_configs)
dag = ea_etl_dag.build(EADagBuildConfigs.EA_ETL_DAG_BUILD_CONFIGS)

# print("Built EA ETL DAG:", built_ea_etl_dag)

