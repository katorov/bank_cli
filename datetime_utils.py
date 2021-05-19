import datetime

BASE_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def string_to_datetime(raw_dt: str) -> datetime.datetime:
    """Convert string to datetime"""
    dt = datetime.datetime.strptime(raw_dt, BASE_DATETIME_FORMAT)
    return dt


def datetime_to_string(dt: datetime.datetime) -> str:
    """Convert datetime to string"""
    raw_dt = dt.strftime(BASE_DATETIME_FORMAT)
    return raw_dt


class DatetimeRange:
    def __init__(self, dt1: datetime.datetime = None, dt2: datetime.datetime = None):
        self._dt1 = dt1
        self._dt2 = dt2

    def __contains__(self, dt):
        if not self._dt1 and not self._dt2:
            return True
        if not self._dt1:
            return dt <= self._dt2
        if not self._dt2:
            return self._dt1 <= dt
        return self._dt1 <= dt <= self._dt2
