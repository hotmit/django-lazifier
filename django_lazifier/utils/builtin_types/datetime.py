import calendar
from datetime import tzinfo, datetime, time, date
from django.utils import timezone
from django_lazifier.utils.utils import log_exception


class Dt:
    @classmethod
    def get_current_tz(cls, ):
        """
        Return django current timezone
        :return:
        """
        return timezone.get_current_timezone()

    @classmethod
    def get_datetime(cls, datetime_str, expected_formats, tz_info: tzinfo = None, default_value=None):
        """
        Get the datetime object if valid, else return None
        :type expected_formats: str|list
        :param datetime_str:
        :param expected_formats: either one format str or a list of acceptable formats
        :return:
        """
        if not datetime_str:
            return default_value

        try:
            if type(expected_formats) is str:
                expected_formats = [expected_formats]

            dt = None
            for f in expected_formats:
                try:
                    dt = datetime.strptime(datetime_str, f)
                except ValueError:
                    dt = None
                if dt is not None:
                    break

            if dt is None:
                return default_value

            if tz_info is not None:
                dt = cls.replace_tzinfo(dt, tz_info)
            return dt
        except ValueError:
            return default_value

    @classmethod
    def is_valid(cls, datetime_str, expected_format):
        """
        Check see if datetime string match the expected format.
        :param datetime_str:
        :param expected_format: eg. '%Y/%m/%d %H:%M:%S'
        :return:
        """
        if Dt.get_datetime(datetime_str, expected_format):
            return True
        return False

    @classmethod
    def get_time(cls, time_str: str, expected_formats, default_value=None):
        """
        Try to parse the time string using specified formats.

        :param time_str:
        :param expected_formats {tuple|list}:
        :param default_value:
        :return:
        """
        for tf in expected_formats:
            try:
                time_value = datetime.strptime(time_str, tf)
                if time_value:
                    return time_value.time()
            except:
                pass
        return default_value

    @classmethod
    def localize_datetime(cls, date_time: datetime, from_tz: tzinfo, to_tz: tzinfo, include_tzinfo=False):
        date_time = cls.replace_tzinfo(date_time, from_tz)
        date_time = date_time.astimezone(to_tz)
        if not include_tzinfo:
            date_time = date_time.replace(tzinfo=None)
        return date_time

    @classmethod
    def localize_time(cls, the_time: time, from_tz: tzinfo, to_tz: tzinfo, include_tzinfo=False):
        """
        Convert time from one timezone to another.

        :param the_time: the time
        :param to_tz: the local time
        :param from_tz: the target timezone
        :param include_tzinfo: include tzinfo along with the result time or not
        :return: {datetime.time}
        """

        if the_time is None or not isinstance(the_time, time):
            return the_time

        dt = datetime.combine(datetime.today().date(), the_time)
        dt = from_tz.localize(dt)  # put timezone on the datetime, convert naive to aware
        tz_dt = dt.astimezone(to_tz)  # convert from_tz to to_tz
        tz_dt = to_tz.normalize(tz_dt)  # take care of dst

        if not include_tzinfo:
            tz_dt = tz_dt.replace(tzinfo=None)  # remove tzinfo

        return tz_dt.time()

    @classmethod
    def diff_in_minutes(cls, datetime_start: datetime, datetime_end: datetime, default_value=-1, round_result=True):
        if not datetime_start or not datetime_end:
            return default_value

        try:
            diff = datetime_end - datetime_start
            total_minutes = diff.total_seconds() / 60
            if round_result:
                total_minutes = int(round(total_minutes, 0))
            return total_minutes
        except Exception as ex:
            log_exception(ex)
            return default_value

    @classmethod
    def diff_in_days(cls, datetime_start: datetime, datetime_end: datetime, default_value=-1):
        """
        Days of (end - start)

        :param datetime_start:
        :param datetime_end:
        :param default_value:
        :return:
        """
        if not datetime_start or not datetime_end:
            return default_value

        try:
            diff = datetime_end - datetime_start
            return diff.days
        except Exception as ex:
            log_exception(ex)
            return default_value

    @classmethod
    def to_sql(cls, dt):
        """
        ISO 8601, MySql date, yyyy-mm-dd hh-mm-ss[.mmm] (24hours)
        :param dt:
        :return:
        """
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def to_postgres_sql_with_tz(cls, dt):
        """
        ISO 8601 with timezone:
            1999-01-08 04:05:06 -8:00,  tz can be +hh:mm, +hhmm, or +hh
            January 8 04:05:06 1999 PST

        :param dt:
        :return:
        """
        return dt.strftime('%Y-%m-%d %H:%M:%S %z').strip()

    @classmethod
    def from_sql(cls, datetime_str, tz_info=None):
        return Dt.get_datetime(datetime_str, '%Y-%m-%d %H:%M:%S', tz_info=tz_info)

    @classmethod
    def to_display_date(cls, dt):
        return dt.strftime('%Y/%m/%d %H:%M:%S')

    @classmethod
    def replace_tzinfo(cls, dt: datetime, tzinfo: tzinfo, is_dst=True):
        """
        This method does not convert timezone, it simply set the timezone to specified timezone.
        :param date_time: if this datetime has tzinfo, it will be overridden
        :param tzinfo: timezone
        :rtype: datetime
        """

        # datetime.replace(tzinfo=user_tz)  => sometime this change the datetime value
        # http://stackoverflow.com/questions/27531718/datetime-timezone-conversion-using-pytz
        # use localize instead

        if dt.tzinfo is not None:
            dt = dt.replace(tzinfo=None)

        local = tzinfo.localize(dt, is_dst=is_dst)
        return tzinfo.normalize(local)

    @classmethod
    def convert_tz(cls, dt, timezone, is_dst=True):
        assert dt.tzinfo, 'The datetime must be time aware, tzinfo cannot be None'

        src_tz = dt.tzinfo
        local_dt = dt.replace(tzinfo=None)
        src_dt = src_tz.normalize(src_tz.localize(local_dt, is_dst=is_dst))
        return src_dt.astimezone(timezone)

    @classmethod
    def to_epoch(cls, dt, default_value=None):
        """
        Convert date or datetime into epoch

        :type dt: {date|datetime}
        :param default_value:
        :rtype: int
        """
        if dt is None or (not isinstance(dt, date) and not isinstance(dt, datetime)):
            return default_value

        if isinstance(dt, date):
            dt = datetime.combine(dt, datetime.min.time())

        origin = datetime(1970, 1, 1)
        if dt.tzinfo is not None:
            origin = cls.replace_tzinfo(origin, timezone.utc)
        return int((dt - origin).total_seconds())

    @classmethod
    def from_epoch(cls, epoch):
        """
        Covert epoch into datetime object (utc)
        :rtype epoch: {int|float}
        :rtype: datetime
        """
        if epoch is not None:
            return datetime.utcfromtimestamp(epoch)
        return None

    @classmethod
    def get_first_day_of_month(cls, dt, replace_time=True):
        if dt is None:
            return None
        dt = dt.replace(day=1)
        if replace_time:
            dt = dt.replace(hour=0, minute=0, second=0)
        return dt

    @classmethod
    def get_last_day_of_month(cls, dt, replace_time=True):
        """
        return the date at the end of the specified datetime's month

        :type dt: {datetime}
        :param replace_time:
        :rtype: datetime
        """
        if dt is None:
            return None
        month, last_day_of_month = calendar.monthrange(dt.year, dt.month)
        dt = dt.replace(day=last_day_of_month)
        if replace_time:
            dt = dt.replace(hour=23, minute=59, second=59)
        return dt

    @classmethod
    def get_first_and_last_day_of_month(cls, dt, replace_time=True):
        """
        return (first, last) tuple

        :param dt:
        :param replace_time:
        :rtype: tuple
        """
        first = cls.get_first_day_of_month(dt, replace_time)
        last = cls.get_last_day_of_month(dt, replace_time)
        return first, last
