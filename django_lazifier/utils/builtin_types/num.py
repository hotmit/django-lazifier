from decimal import Decimal


class Num:

    @classmethod
    def round(cls, number, decimal_places):
        """
        Round a float number

        :param number:
        :param decimal_places:
        :return:
        """
        num = Decimal(number)       # use decimal to prevent super large number from overflowing
        multiplier = 10 * decimal_places

        num = round(num * multiplier) / multiplier
        return float(num)

    @classmethod
    def as_money(cls, amount):
        """
        Format the specified number as money string format (does not support i10n)

        :param amount: the float number
        :rtype : str
        """
        amount = float(amount)
        return '${:.2f}'.format(amount).rstrip('0').rstrip('.')
