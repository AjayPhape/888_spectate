from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView

from base.error_codes import ErrorCodes
from base.utils import DBCursor


# update your views here.

class UpdateSport(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def update_sport(data):
        name = data.get('name')
        slug = data.get('slug')
        active = data.get('active')
        sport_id = data.get('id')
        resp = ErrorCodes.get_error_response(200)

        with DBCursor() as cr:
            current_utc_time = datetime.utcnow()
            modified_at = current_utc_time.strftime("%Y-%m-%d %H:%M:%S")

            qry = """
                UPDATE base_sport
                SET
                    name = %s,
                    slug = %s,
                    active = %s,
                    modified_at = %s
                WHERE
                    id = %s
            """
            cr.execute(
                qry, [name, slug, active, modified_at, sport_id]
            )

            # check if update is successful
            if cr.rowcount == 0:
                return ErrorCodes.get_error_response(301)
        return resp

    def post(self, request, *args, **kwargs):
        resp = self.update_sport(request.data)
        return Response(resp)


class UpdateEvent(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def check_event_status(event_id, cr, resp=None):
        # check if there is any active event for sport
        if not resp:
            resp = ErrorCodes.get_error_response(200)

        qry = """
            SELECT SUM(case when active then 1 else 0 end), sport_id
            FROM base_event be
            WHERE sport_id = (SELECT sport_id FROM base_event be2 WHERE id = %s)
        """
        cr.execute(
            qry, [event_id]
        )
        event_count, sport_id = cr.fetchone()
        # disable the sport if no event active
        if event_count == 0:
            qry = "UPDATE base_sport SET active = false WHERE id = %s"
            cr.execute(qry, [sport_id])
            resp = {**resp, 'responseMessage': 'Sport disabled due to no events'}
        return resp

    @classmethod
    def update_event(cls, data):
        # resp = ErrorCodes.get_error_response(500)
        name = data.get('name')
        slug = data.get('slug')
        active = data.get('active')
        scheduled_start = data.get('scheduled_start')
        actual_start = data.get('actual_start')
        event_id = data.get('id')
        event_type = data.get('event_type')
        status = data.get('status')

        with DBCursor() as cr:
            current_utc_time = datetime.utcnow()
            modified_at = current_utc_time.strftime("%Y-%m-%d %H:%M:%S")
            qry = """
                UPDATE base_event
                SET
                    name = %s,
                    slug = %s,
                    active = %s,
                    scheduled_start = %s,
                    actual_start = %s,
                    event_type = %s,
                    status = %s,
                    modified_at = %s
                WHERE
                    id = %s
            """
            cr.execute(
                qry, [name, slug, active, scheduled_start, actual_start, event_type, status, modified_at, event_id]
            )
            # check if update is successful
            if cr.rowcount == 0:
                return ErrorCodes.get_error_response(301)

            resp = cls.check_event_status(event_id, cr)
            return resp

    def post(self, request, *args, **kwargs):
        resp = self.update_event(request.data)
        return Response(resp)


class UpdateSelection(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def check_selection_status(selection_id, cr):
        # check if there is any active selection for event
        resp = ErrorCodes.get_error_response(200)
        qry = """
            SELECT SUM(case when active then 1 else 0 end), event_id
            FROM base_selection bs 
            WHERE event_id = (SELECT event_id FROM base_selection bs2 WHERE id = %s)
          """
        cr.execute(
            qry, [selection_id]
        )
        selection_count, event_id = cr.fetchone()
        # disable the event if no selection active
        if selection_count == 0:
            qry = "UPDATE base_event SET active = false WHERE id = %s"
            cr.execute(qry, [event_id])
            resp = {**resp, 'responseMessage': 'Event disabled due to no events'}
            resp = UpdateEvent.check_event_status(event_id, cr, resp)
        return resp

    @classmethod
    def update_selection(cls, data):
        resp = ErrorCodes.get_error_response(500)
        name = data.get('name')
        active = data.get('active')
        outcome = data.get('outcome')
        price = data.get('price')
        selection_id = data.get('id')

        with DBCursor() as cr:
            current_utc_time = datetime.utcnow()
            modified_at = current_utc_time.strftime("%Y-%m-%d %H:%M:%S")
            qry = """
                UPDATE base_selection
                SET
                    name = %s,
                    active = %s,
                    price = %s,
                    outcome = %s,
                    modified_at = %s
                WHERE
                    id = %s
            """
            cr.execute(
                qry, [name, active, price, outcome, modified_at, selection_id]
            )

            # check if update is successful
            if cr.rowcount == 0:
                return ErrorCodes.get_error_response(301)
            resp = cls.check_selection_status(selection_id, cr)
            return resp

    def post(self, request, *args, **kwargs):
        resp = self.update_selection(request.data)
        return Response(resp)
