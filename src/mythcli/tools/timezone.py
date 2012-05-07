from datetime import tzinfo, timedelta, datetime

def strflocaltime(datetime, stringformat):
    """ Return formatted local time string. @stringformat: format string or None """
    utcoffset_td = local.utcoffset(datetime)
    if stringformat:
        string = (datetime + utcoffset_td).strftime(stringformat)
    else:
        string = str(datetime + utcoffset_td)
    return string

####

ZERO = timedelta(0)
HOUR = timedelta(hours=1)

# A UTC class.
class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

utc = UTC()

####

# A class building tzinfo objects for fixed-offset time zones.
# Note that FixedOffset(0, "UTC") is a different way to build a
# UTC tzinfo object.
class FixedOffset(tzinfo):
    """Fixed offset in minutes east from UTC."""

    def __init__(self, offset, name):
        self.__offset = timedelta(minutes=offset)
        self.__name = name

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return ZERO

####

import time as _time

STDOFFSET = timedelta(seconds= -_time.timezone)
if _time.daylight:
    DSTOFFSET = timedelta(seconds= -_time.altzone)
else:
    DSTOFFSET = STDOFFSET

DSTDIFF = DSTOFFSET - STDOFFSET

# A class capturing the platform's idea of local time.
class LocalTimezone(tzinfo):

    def utcoffset(self, dt):
        if self._isdst(dt):
            return DSTOFFSET
        else:
            return STDOFFSET

    def dst(self, dt):
        if self._isdst(dt):
            return DSTDIFF
        else:
            return ZERO

    def tzname(self, dt):
        return _time.tzname[self._isdst(dt)]

    def _isdst(self, dt):
        tt = (dt.year, dt.month, dt.day,
              dt.hour, dt.minute, dt.second,
              dt.weekday(), 0, 0)
        stamp = _time.mktime(tt)
        tt = _time.localtime(stamp)
        return tt.tm_isdst > 0

local = LocalTimezone()
