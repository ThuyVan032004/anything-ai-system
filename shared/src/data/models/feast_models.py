from datetime import timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
from feast import Entity, Field, FileSource, KafkaSource
from feast.data_format import JsonFormat, ParquetFormat
from feast.data_source import PushMode

import pandas as pd
from pydantic import BaseModel
from src.common.models import TagModel


class FeastFileSourceModel(BaseModel):
    name: str
    file_format: str
    path: ParquetFormat
    timestamp_field: Optional[str] = None
    created_timestamp_column: Optional[str] = None
    
class FeastKafkaSourceModel(BaseModel):
    name: str
    kafka_bootstrap_servers: str
    topic: str
    message_format: str
    timestamp_field: Optional[str] = None
    batch_source: JsonFormat
    batch_source: Optional[str] = None
    description: Optional[str] = None
    
class FeastFeatureViewModel(BaseModel):
    name: str
    entities: List[Entity]
    ttl: Optional[timedelta] = None
    description: Optional[str] = None
    schema: List[Field]
    online: bool = True
    source: KafkaSource | FileSource
    tags: Optional[List[TagModel]] = None
    timestamp_field: Optional[str] = None
    
class FeastGetHistoricalFeaturesModel(BaseModel):
    entity_df: pd.DataFrame
    features: List[str]
    
class FeastGetStreamFeaturesModel(BaseModel):
    features: List[str]
    entity_rows: List[Dict[str, Any]]

class FeastPushToFeatureStoreModel(BaseModel):
    source_name: str
    df: pd.DataFrame
    to: Enum



