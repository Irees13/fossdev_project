import unittest
from decimal import Decimal
from converter.core import convert_currency, UnsupportedCurrencyError, InvalidAmountError

class TestCoreLogic(unittest.TestCase):
    def setUp(self):
        self.rates = {
            "USD": Decimal("1.0"),
            "EUR": Decimal("0.9"),
            "RUB": Decimal("90.0")
        }

    def test_direct_conversion(self):
        res = convert_currency("USD", "RUB", Decimal("10.00"), self.rates, Decimal("0.02"))
        self.assertEqual(res["raw_converted"], Decimal("900.00"))
        self.assertEqual(res["fee"], Decimal("18.00"))
        self.assertEqual(res["final_amount"], Decimal("882.00"))

    def test_negative_amount_raises(self):
        with self.assertRaises(InvalidAmountError):
            convert_currency("USD", "RUB", Decimal("-10.00"), self.rates)

    def test_unsupported_currency_raises(self):
        with self.assertRaises(UnsupportedCurrencyError):
            convert_currency("USD", "KZT", Decimal("10.00"), self.rates)

if __name__ == "__main__":
    unittest.main()