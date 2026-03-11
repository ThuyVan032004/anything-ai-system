from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class DagDockerTaskModel(BaseModel):
    task_id: str
    image: str
    api_version: Optional[str] = "auto"
    auto_remove: Optional[str] = "force"
    command: str
    docker_url: Optional[str] = "tcp://docker-proxy:2375"
    network_mode: Optional[str] = "shared-network"
    mount_tmp_dir: Optional[bool] = False
    environment: Optional[Dict[str, str]] = None
    device_requests: Optional[List[Any]] = [
        {
            "driver": "nvidia",
            "count": -1,  # Sử dụng tất cả GPU có sẵn
            "capabilities": [["gpu"]]
        }
    ]
