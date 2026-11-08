import pytest
import asyncio
from services.validation_service import ValidationService

def test_validation_empty_product():
    with pytest.raises(ValueError, match="El ID del producto no puede estar vacío."):
        ValidationService.validate_movement_input("", "Bodega SCL", 10)

def test_validation_zero_quantity():
    with pytest.raises(ValueError, match="La cantidad a mover no puede ser cero."):
        ValidationService.validate_movement_input("PROD01", "Bodega SCL", 0)