"""Маршрутизація замовлень: вибір кур'єра, ETA та надбавки."""


def route_order(order, couriers, hour, is_vip, surge):
    plan = {"courier": None, "priority": 0, "eta_min": 30, "fee": 0.0}
    if not couriers:
        plan["priority"] = -1
        return plan
    if is_vip:
        plan["priority"] += 2
    if order["distance_km"] > 10:
        plan["eta_min"] += 20
    elif order["distance_km"] > 5:
        plan["eta_min"] += 10
    if hour >= 22 or hour < 6:
        plan["fee"] += 15.0
    if surge > 1.5:
        plan["fee"] = plan["fee"] * surge
    if order["total"] > 1000 and is_vip:
        plan["fee"] = 0.0
    if order.get("fragile"):
        plan["eta_min"] += 5
    return plan
