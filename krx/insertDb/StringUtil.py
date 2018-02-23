from datetime import datetime, timedelta

def strCommaToInt(str):
    str = str.replace(',', '')
    return int(str)

def change_hour_minute(date, hours, minutes):
    date = date.replace(hour=hours, minute=minutes)
    return date
