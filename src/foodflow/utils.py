"""Допоміжні функції."""


def format_price(amount, currency="UAH"):
    return f"{amount:.2f} {currency}"


def clamp(value, low, high):
    return max(low, min(value, high))
