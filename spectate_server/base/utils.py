from datetime import datetime

import pytz
from django.db import connection


class DBCursor:

    def __init__(self):
        self.cursor = connection.cursor()
        self.rowcount = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.cursor.close()

    def execute(self, query, params=None):
        params = params or []
        res = self.cursor.execute(query, params)
        self.rowcount = self.cursor.rowcount
        return res

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def dictfetchall(self):
        """Returns all rows from a cursor as a dict"""
        result = self.fetchall()

        if result:
            col_list = [col[0] for col in self.cursor.description]
            return [dict(zip(col_list, row)) for row in result]
        return []


def is_timezone_valid(timezone_option):
    try:
        pytz.timezone(timezone_option)
        return True
    except pytz.exceptions.UnknownTimeZoneError:
        return False


def convert_tz(original_datetime, to_tz='utc'):
    original_datetime = datetime.strptime(original_datetime, "%Y-%m-%d %H:%M:%S%z")
    print("Original datetime:", original_datetime)

    # Convert the datetime to a different time zone
    target_timezone = pytz.timezone(to_tz)
    converted_datetime = original_datetime.astimezone(target_timezone)
    converted_datetime_str = converted_datetime.strftime("%Y-%m-%d %H:%M")
    return converted_datetime, converted_datetime_str
