class ValidationService:
    @staticmethod
    def validate_movement_input(product_id: str, warehouse_id: str, quantity: int):
        if not product_id or not product_id.strip():
            raise ValueError("El ID del producto no puede estar vacío.")
        if not warehouse_id or not warehouse_id.strip():
            raise ValueError("La bodega no puede estar vacía.")
        if quantity == 0:
            raise ValueError("La cantidad a mover no puede ser cero.")