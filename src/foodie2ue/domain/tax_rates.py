from decimal import Decimal

RATES = {
    '80523': Decimal('2.25'),
    '80534': Decimal('5.25'),
    '12345': Decimal('3.25'),
}


def get_tax_rate_by_zip(zip_code: str) -> Decimal:
    return RATES.get(zip_code, Decimal('0'))
