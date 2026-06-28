"""Заглушка платіжного шлюзу (у продакшні — запит до зовнішнього REST API)."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ChargeResult:
    token: str
    user_id: str
    amount: float


def charge_card(token, amount, user_id):
    return ChargeResult(token=token, user_id=user_id, amount=amount)
