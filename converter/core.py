from decimal import Decimal, ROUND_HALF_UP
from typing import Dict

class ExchangeError(Exception):
    pass

class UnsupportedCurrencyError(ExchangeError):
    pass

class InvalidAmountError(ExchangeError):
    pass

def convert_currency(
    source: str,
    target: str,
    amount: Decimal,
    rates: Dict[str, Decimal],
    fee_rate: Decimal = Decimal("0.01")
) -> dict:
    if amount <= Decimal("0"):
        raise InvalidAmountError("Amount must be positive")
    
    if source not in rates or target not in rates:
        raise UnsupportedCurrencyError(
            f"Unsupported currency. Supported: {list(rates.keys())}"
        )

    # Расчет через базовый USD
    amount_in_usd = amount / rates[source]
    converted_amount = amount_in_usd * rates[target]
    
    fee = converted_amount * fee_rate
    final_amount = converted_amount - fee

    cents = Decimal("0.01")
    rate_precision = Decimal("0.000001")
    
    return {
        "source": source,
        "target": target,
        "amount": amount.quantize(cents, rounding=ROUND_HALF_UP),
        "rate": (rates[target] / rates[source]).quantize(rate_precision, rounding=ROUND_HALF_UP),
        "raw_converted": converted_amount.quantize(cents, rounding=ROUND_HALF_UP),
        "fee": fee.quantize(cents, rounding=ROUND_HALF_UP),
        "final_amount": final_amount.quantize(cents, rounding=ROUND_HALF_UP)
    }