"""Checkout: розрахунок суми замовлення та списання через платіжний шлюз."""
from .payment_gateway import charge_card


def checkout(user_id: str, token: str, dish: dict, discount_pct: float,
             delivery_fee: float, tax_rate: float, currency: str, fx_rate: float):
    if discount_pct > 0:
        dish["price"] = dish["price"] * (1 - discount_pct / 100)
    total = dish["price"] * dish["qty"]
    total = total + delivery_fee
    total = total * (1 + tax_rate)
    if currency != "UAH":
        total = total * fx_rate
    return charge_card(token, round(total, 2), user_id)
