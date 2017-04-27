from datetime import tzinfo, datetime, time
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
                dt = dt.replace(tzinfo=tz_info)
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
    def localize_datetime(cls, date_time: datetime, from_tz: tzinfo, to_tz: tzinfo, include_tzinfo=False):
        date_time = date_time.replace(tzinfo=from_tz)
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
        return dt.strftime('%Y-%m-%d %H:%M:%S %Z').strip()

    @classmethod
    def from_sql(cls, datetime_str, tz_info=None):
        return Dt.get_datetime(datetime_str, '%Y-%m-%d %H:%M:%S', tz_info=tz_info)

    @classmethod
    def to_display_date(cls, dt):
        return dt.strftime('%Y/%m/%d %H:%M:%S')
