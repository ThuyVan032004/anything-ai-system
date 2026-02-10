from src.pipeline.etl_dag_base import ETLDagBase
from src.pipeline.models.dag_config_model import DagConfigModel
from src.pipeline.models.dag_etl_build_model import DagETLBuildModel


class EAETLDag(ETLDagBase):
    def __init__(self, configs: DagConfigModel):
        super().__init__(configs)
        
    def build(self, build_configs: DagETLBuildModel):
        return super().build(build_configs)
    

ea_etl_dag_configs = DagConfigModel(
    dag_id="ea_etl_dag"
)

ea_etl_dag = EAETLDag(ea_etl_dag_configs)
built_ea_etl_dag = ea_etl_dag.build()


