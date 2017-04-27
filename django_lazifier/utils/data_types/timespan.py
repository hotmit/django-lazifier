from datetime import timedelta


class TimeSpan(timedelta):
    """
    The extension of timedelta
    """
    def __init__(self, time_delta=None, total_seconds=None):
        if total_seconds:
            self.timedelta = timedelta(seconds=int(total_seconds))
        elif time_delta and isinstance(time_delta, timedelta):
            self.timedelta = time_delta

    @property
    def years(self):
        return self.timedelta.days / 365

    @property
    def months(self):
        return self.timedelta.days / 30

    @property
    def weeks(self):
        return self.timedelta.days / 7

    @property
    def days(self):
        return self.timedelta.days

    @property
    def hours(self):
        return self.timedelta.seconds / 3600

    @property
    def minutes(self):
        return self.timedelta.seconds / 60

    @property
    def seconds(self):
        return self.timedelta.seconds

    @property
    def milliseconds(self):
        return self.timedelta.microseconds / 1000

    @property
    def microseconds(self):
        return self.timedelta.microseconds
