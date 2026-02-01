from typing import Optional
from pydantic import BaseModel

from pendulum import DateTime


class DagDefaultArgsModel(BaseModel):
    owner: str
    retries: int
    retry_delay: int # in seconds

class DagConfigModel(BaseModel):
    dag_id: str
    default_args: Optional[DagDefaultArgsModel]
    schedule_interval: Optional[str]
    start_date: Optional[DateTime]
    catchup: Optional[bool]
    tags: Optional[list[str]] 
    max_active_runs: Optional[int]
    