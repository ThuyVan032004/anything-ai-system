from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class DagDefaultArgsModel(BaseModel):
    owner: str
    retries: int
    retry_delay: int # in seconds

class DagConfigModel(BaseModel):
    dag_id: str
    default_args: Optional[DagDefaultArgsModel] = None
    schedule: Optional[str] = "@once"
    start_date: Optional[datetime] = datetime(2026, 1, 1)
    catchup: Optional[bool] = False
    tags: Optional[list[str]] = None
    max_active_runs: Optional[int] = None
    