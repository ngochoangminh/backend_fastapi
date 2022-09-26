import pytz
from datetime import datetime, timedelta

def datetime_to_epoch_ms(dt):
    epoch = datetime.utcfromtimestamp(0)
    utc_dt = dt.astimezone(pytz.utc)
    utc_dt = utc_dt.replace(tzinfo=None)
    return int((utc_dt - epoch).total_seconds() * 1000.0)

def validator_datetime_utc(dt: datetime):
    if not isinstance(dt, datetime):
        return dt
    if dt.tzinfo is None:
        return dt.replace(tzinfo=pytz.utc)
    utc_dt = dt.astimezone(pytz.utc)
    return utc_dt

def format_utc_str(dt: datetime):
    dt = validator_datetime_utc(dt)
    return dt.isoformat()

def today_timestamp(hour:int = 0, minute:int = 0, second:int = 0, microsecond: int = 0) -> float|None:
    return datetime.today().replace(hour=hour, minute=minute, second=second, microsecond=microsecond).timestamp()

def relative_timestamp(datetime_from: datetime|float, days: int = 0, hours: int = 0, minutes:int = 0, seconds:int = 0, microseconds: int = 0) -> float|None:
    match datetime_from:
        case datetime():
            return (datetime_from + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds, microseconds=microseconds)).timestamp()
        case float():
            return (datetime.fromtimestamp(datetime_from) + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds, microseconds=microseconds)).timestamp()
        case _:
            return None