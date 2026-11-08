from dataclasses import dataclass
from datetime import datetime

@dataclass
class Movement:
    product_id: str
    warehouse_id: str
    delta: int
    id: int = None
    timestamp: datetime = None