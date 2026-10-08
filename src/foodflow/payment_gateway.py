"""Заглушка платіжного шлюзу (у продакшні — запит до зовнішнього REST API)."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ChargeResult:
    token: str
    user_id: str
    amount: float
    status: str = "OK"


def charge_card(token, amount, user_id):
    if amount <= 0:
        raise ValueError("amount must be positive")
    if not token:
        raise ValueError("token is required")
    return ChargeResult(token=token, user_id=user_id, amount=amount)
