from dataclasses import dataclass

@dataclass
class Warehouse:
    warehouse_id: str
    name: str
    location: str = ""