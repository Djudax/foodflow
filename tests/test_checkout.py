import unittest

from foodflow.checkout import checkout


def make_dish():
    return {"name": "Борщ", "price": 100.0, "qty": 2}


class CheckoutBaseline(unittest.TestCase):
    def test_first_call_total(self):
        result = checkout("u1", "tok_1", make_dish(), 10, 30.0, 0.2, "UAH", 1.0)
        self.assertEqual(result.amount, 252.0)

    def test_foreign_currency(self):
        dish = {"name": "Борщ", "price": 50.0, "qty": 1}
        result = checkout("u1", "tok_1", dish, 0, 0.0, 0.0, "USD", 41.0)
        self.assertEqual(result.amount, 2050.0)


class MutationCrashTest(unittest.TestCase):
    """Краш-тест: повторний запит (retry після таймауту шлюзу) з тим самим об'єктом."""

    def test_retry_charges_same_amount(self):
        dish = make_dish()
        first = checkout("u1", "tok_1", dish, 10, 30.0, 0.2, "UAH", 1.0)
        second = checkout("u1", "tok_1", dish, 10, 30.0, 0.2, "UAH", 1.0)
        self.assertEqual(first.amount, second.amount)

    def test_base_price_is_not_overwritten(self):
        dish = make_dish()
        checkout("u1", "tok_1", dish, 10, 30.0, 0.2, "UAH", 1.0)
        self.assertEqual(dish["price"], 100.0)


if __name__ == "__main__":
    unittest.main()
