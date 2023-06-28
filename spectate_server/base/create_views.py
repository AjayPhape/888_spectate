from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView

from base.error_codes import ErrorCodes
from base.utils import DBCursor


# Create your views here.
def get_last_inserted_id(cr):
    cr.execute('SELECT last_insert_rowid() AS new_id')
    return cr.fetchone()[0]


class CreateSport(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def create_sport(data):
        resp = ErrorCodes.get_error_response(200)
        name = data.get('name')
        slug = data.get('slug')
        active = data.get('active')

        with DBCursor() as cr:
            current_utc_time = datetime.utcnow()
            time_now = current_utc_time.strftime("%Y-%m-%d %H:%M:%S")

            qry = """
                INSERT INTO 
                    base_sport (name, slug, active, created_at, modified_at) 
                VALUES 
                    (%s, %s, %s, %s, %s)
            """
            cr.execute(
                qry, [name, slug, active, time_now, time_now]
            )

            # check if insertion is successful
            if cr.rowcount == 0:
                resp = ErrorCodes.get_error_response(500)
            rec_id = get_last_inserted_id(cr)
            return {**resp, 'id': rec_id}

    def post(self, request, *args, **kwargs):
        resp = self.create_sport(request.data)
        return Response(resp)


class CreateEvent(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def is_sport_exists(sport_id, cr):
        # check if record exists in system or not
        qry = """
            SELECT EXISTS (
                SELECT id
                FROM base_sport
                WHERE id = %s
            )
        """
        cr.execute(qry, [sport_id])
        row_count = cr.fetchone()[0]
        return row_count

    @classmethod
    def create_event(cls, data):
        resp = ErrorCodes.get_error_response(200)
        name = data.get('name')
        slug = data.get('slug')
        active = data.get('active')
        scheduled_start = data.get('scheduled_start')
        actual_start = data.get('actual_start')
        sport_id = data.get('sport_id')
        event_type = data.get('event_type')
        status = data.get('status')

        with DBCursor() as cr:
            row_count = cls.is_sport_exists(sport_id, cr)
            if not row_count:
                return ErrorCodes.get_error_response(300)

            current_utc_time = datetime.utcnow()
            time_now = current_utc_time.strftime("%Y-%m-%d %H:%M:%S")
            qry = """
                INSERT INTO 
                    base_event (name, slug, active, scheduled_start, actual_start, event_type, status, sport_id, created_at, modified_at)
                VALUES 
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cr.execute(
                qry,
                [name, slug, active, scheduled_start, actual_start, event_type, status, sport_id, time_now, time_now]
            )
            # check if insertion is successful
            if cr.rowcount == 0:
                resp = ErrorCodes.get_error_response(500)
            rec_id = get_last_inserted_id(cr)
            return {**resp, 'id': rec_id}

    def post(self, request, *args, **kwargs):
        resp = self.create_event(request.data)
        return Response(resp)


class CreateSelection(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def is_event_exists(event_id, cr):
        # check if record exists in system or not
        qry = """
            SELECT EXISTS (
                SELECT id
                FROM base_event
                WHERE id = %s
            )
        """
        cr.execute(qry, [event_id])
        row_count = cr.fetchone()[0]
        return row_count

    @classmethod
    def create_selection(cls, data):
        resp = ErrorCodes.get_error_response(200)
        name = data.get('name')
        active = data.get('active')
        outcome = data.get('outcome')
        price = data.get('price')
        event_id = data.get('event_id')

        with DBCursor() as cr:
            row_count = cls.is_event_exists(event_id, cr)
            if not row_count:
                return ErrorCodes.get_error_response(300)

            current_utc_time = datetime.utcnow()
            time_now = current_utc_time.strftime("%Y-%m-%d %H:%M:%S")
            qry = """
                INSERT INTO 
                    base_selection (name, active, event_id, price, outcome, created_at, modified_at)
                VALUES 
                    (%s, %s, %s, %s, %s, %s, %s)
            """
            cr.execute(
                qry, [name, active, event_id, price, outcome, time_now, time_now]
            )

            # check if insertion is successful
            if cr.rowcount == 0:
                resp = ErrorCodes.get_error_response(500)
            rec_id = get_last_inserted_id(cr)
            return {**resp, 'id': rec_id}

    def post(self, request, *args, **kwargs):
        resp = self.create_selection(request.data)
        return Response(resp)
