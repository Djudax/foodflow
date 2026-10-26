"""Меню ресторанів мережі Gusto."""

MENU = {
    "borscht": {"name": "Борщ", "price": 120.0, "from_hour": 10, "to_hour": 22},
    "varenyky": {"name": "Вареники", "price": 110.0, "from_hour": 10, "to_hour": 22},
    "deruny": {"name": "Деруни", "price": 95.0, "from_hour": 10, "to_hour": 22},
    "chicken_kyiv": {"name": "Котлета по-київськи", "price": 190.0, "from_hour": 11, "to_hour": 23},
    "pizza_margherita": {"name": "Піца Маргарита", "price": 210.0, "from_hour": 11, "to_hour": 23},
    "caesar": {"name": "Цезар", "price": 175.0, "from_hour": 11, "to_hour": 22},
    "ramen": {"name": "Рамен", "price": 230.0, "from_hour": 12, "to_hour": 23},
    "burger": {"name": "Бургер", "price": 205.0, "from_hour": 11, "to_hour": 23},
    "cheesecake": {"name": "Чізкейк", "price": 120.0, "from_hour": 10, "to_hour": 23},
    "lemonade": {"name": "Лимонад", "price": 70.0, "from_hour": 10, "to_hour": 23},
    "espresso": {"name": "Еспресо", "price": 55.0, "from_hour": 8, "to_hour": 22},
    "tiramisu": {"name": "Тірамісу", "price": 140.0, "from_hour": 11, "to_hour": 23},
}


def find_dish(code):
    return MENU.get(code)


def is_available(code, hour):
    dish = MENU.get(code)
    if dish is None:
        return False
    return dish["from_hour"] <= hour < dish["to_hour"]
