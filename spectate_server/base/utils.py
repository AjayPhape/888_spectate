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
