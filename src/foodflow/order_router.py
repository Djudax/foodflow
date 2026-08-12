"""Маршрутизація замовлень: вибір кур'єра, ETA та надбавки."""


def route_order(order, couriers, hour, is_vip, surge):
    plan = {"courier": None, "priority": 0, "eta_min": 30, "fee": 0.0}
    if not couriers:
        plan["priority"] = -1
        return plan
    return plan
