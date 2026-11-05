import unittest
from dataclasses import FrozenInstanceError

from foodflow.checkout import checkout
from foodflow.models import Order, OrderLine, PricingTerms


def make_order(**overrides):
    terms = dict(discount_pct=10, delivery_fee=30.0, tax_rate=0.2)
    terms.update(overrides)
    return Order(OrderLine("Борщ", 100.0, 2), PricingTerms(**terms))


class CheckoutBaseline(unittest.TestCase):
    def test_first_call_total(self):
        result = checkout("u1", "tok_1", make_order())
        self.assertEqual(result.amount, 252.0)

    def test_foreign_currency(self):
        order = Order(OrderLine("Борщ", 50.0, 1), PricingTerms(currency="USD", fx_rate=41.0))
        self.assertEqual(checkout("u1", "tok_1", order).amount, 2050.0)


class MutationCrashTest(unittest.TestCase):
    """Той самий краш-тест, що був FAIL: тепер сценарій проходить (PASS)."""

    def test_retry_charges_same_amount(self):
        order = make_order()
        first = checkout("u1", "tok_1", order)
        second = checkout("u1", "tok_1", order)
        self.assertEqual(first.amount, second.amount)

    def test_base_price_is_not_overwritten(self):
        order = make_order()
        checkout("u1", "tok_1", order)
        self.assertEqual(order.line.price, 100.0)


class ImmutabilityAndValidation(unittest.TestCase):
    def test_order_line_is_frozen(self):
        order = make_order()
        with self.assertRaises(FrozenInstanceError):
            order.line.price = 1.0

    def test_discount_out_of_range_is_rejected(self):
        with self.assertRaises(ValueError):
            PricingTerms(discount_pct=100)

    def test_uah_with_exchange_rate_is_rejected(self):
        with self.assertRaises(ValueError):
            PricingTerms(currency="UAH", fx_rate=41.0)


if __name__ == "__main__":
    unittest.main()
