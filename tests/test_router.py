import unittest

from foodflow.order_router import route_order

COURIERS = [{"id": "c1", "free": True, "rating": 5.0}]


def make_order(**overrides):
    order = {"distance_km": 3, "total": 300.0}
    order.update(overrides)
    return order


class RouteOrderTest(unittest.TestCase):
    def test_no_couriers_gets_negative_priority(self):
        plan = route_order(make_order(), [], 12, False, 1.0)
        self.assertEqual(plan["priority"], -1)

    def test_vip_gets_higher_priority(self):
        plan = route_order(make_order(), COURIERS, 12, True, 1.0)
        self.assertEqual(plan["priority"], 2)

    def test_courier_is_assigned(self):
        plan = route_order(make_order(), COURIERS, 12, False, 1.0)
        self.assertEqual(plan["courier"], "c1")


if __name__ == "__main__":
    unittest.main()
