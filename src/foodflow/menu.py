"""Меню ресторанів мережі Gusto."""

MENU = {
    "borscht": {"name": "Борщ", "price": 120.0, "from_hour": 10, "to_hour": 22},
    "varenyky": {"name": "Вареники", "price": 110.0, "from_hour": 10, "to_hour": 22},
    "deruny": {"name": "Деруни", "price": 95.0, "from_hour": 10, "to_hour": 22},
}


def find_dish(code):
    return MENU.get(code)


def is_available(code, hour):
    dish = MENU.get(code)
    if dish is None:
        return False
    return dish["from_hour"] <= hour < dish["to_hour"]
