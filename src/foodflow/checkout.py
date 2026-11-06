"""Checkout: списання суми замовлення через платіжний шлюз."""
from .models import Order
from .payment_gateway import charge_card


def checkout(user_id: str, token: str, order: Order):
    """Незмінне замовлення -> одне детерміноване списання (безпечно для retry)."""
    return charge_card(token, order.total(), user_id)
