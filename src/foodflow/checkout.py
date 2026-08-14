"""Checkout: розрахунок суми замовлення та списання через платіжний шлюз."""
from .payment_gateway import charge_card


def checkout(user_id, token, dish, discount_pct, delivery_fee):
    if discount_pct > 0:
        dish["price"] = dish["price"] * (1 - discount_pct / 100)
    total = dish["price"] * dish["qty"]
    total = total + delivery_fee
    return charge_card(token, total, user_id)
