from pydantic import BaseModel
from typing import Optional


class TabularMissingValueProps(BaseModel):
    column: str
    method: str  # e.g., 'mean', 'median', 'mode', 'drop', etc.
    fill_value: Optional[float] = None

class TabularOutlierProps(BaseModel):
    column: str
    method: str  # remove, cap, etc.
    
