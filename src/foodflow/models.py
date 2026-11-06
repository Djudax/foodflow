"""Незмінні об'єкти-значення (Value Objects) для checkout."""
from dataclasses import dataclass


@dataclass(frozen=True)
class OrderLine:
    name: str
    price: float
    qty: int = 1

    def subtotal(self) -> float:
        return self.price * self.qty


@dataclass(frozen=True)
class PricingTerms:
    """Усі цінові умови замовлення в одному незмінному контейнері.

    fx_rate — множник до UAH (для UAH має дорівнювати 1.0).
    """
    discount_pct: float = 0.0
    delivery_fee: float = 0.0
    tax_rate: float = 0.0
    currency: str = "UAH"
    fx_rate: float = 1.0

    def __post_init__(self):
        if not 0 <= self.discount_pct < 100:
            raise ValueError("discount_pct must be in [0, 100)")
        if self.fx_rate <= 0:
            raise ValueError("fx_rate must be positive")
        if self.currency == "UAH" and self.fx_rate != 1.0:
            raise ValueError("fx_rate must be 1.0 for UAH")

    def final_amount(self, subtotal: float) -> float:
        return round(
            (subtotal * (1 - self.discount_pct / 100) + self.delivery_fee)
            * (1 + self.tax_rate) * self.fx_rate, 2)


@dataclass(frozen=True)
class Order:
    line: OrderLine
    terms: PricingTerms

    def total(self) -> float:
        return self.terms.final_amount(self.line.subtotal())
