from decimal import Decimal

TWO_PLACES = Decimal("0.01")


def to_paisa(rupees: Decimal) -> int:
    """Rs 150.50 -> 15050. Input is already validated to have at most 2 decimal places."""
    return int((rupees * 100).to_integral_value())


def to_rupees(paisa: int) -> Decimal:
    """15050 -> Decimal('150.50')."""
    return (Decimal(paisa) / 100).quantize(TWO_PLACES)
