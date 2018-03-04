from datetime import datetime, timedelta

def strCommaToInt(str):
    str = str.replace(',', '')
    return int(str)

def change_hour_minute(date, hours, minutes):
    date = date.replace(hour=hours, minute=minutes)
    return date

# timestamp to datetime
def timestamp_to_time(timestamp):
    date = datetime.fromtimestamp(timestamp/1000)
    return date
