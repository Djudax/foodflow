"""Оцінка часу доставки."""


def estimate_delivery(distance_km, traffic, weather, hour, zone, is_rush):
    minutes = 10 + distance_km * 3
    if traffic == "heavy":
        minutes += 15
    elif traffic == "medium":
        minutes += 7
    if weather == "snow" or weather == "storm":
        minutes += 20
    elif weather == "rain":
        minutes += 10
    if zone == "center":
        minutes += 5
    elif zone == "suburb":
        minutes += 10
    if is_rush and 17 <= hour <= 19:
        minutes += 12
    if hour >= 23 or hour < 6:
        minutes -= 5
    return max(minutes, 15)
