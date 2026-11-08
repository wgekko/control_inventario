from dataclasses import dataclass

@dataclass
class Product:
    product_id: str
    warehouse_id: str
    quantity: int
    min_stock: int = 10
    unit_cost: float = 100.0

    @property
    def total_value(self) -> float:
        return self.quantity * self.unit_cost

    @property
    def is_critical(self) -> bool:
        return self.quantity <= self.min_stock