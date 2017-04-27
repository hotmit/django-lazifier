from decimal import Decimal


class Num:

    @classmethod
    def round(cls, number, decimal_places):
        num = Decimal(number)       # use decimal to prevent super large number from overflowing
        multiplier = 10 * decimal_places

        num = round(num * multiplier) / multiplier
        return float(num)
