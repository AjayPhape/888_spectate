import json
import logging
from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView

from base.error_codes import ErrorCodes
from base.serializers import GetSportSerializer
from base.utils import DBCursor, is_timezone_valid, convert_tz

logger = logging.getLogger(__name__)


# get your views here.
# qry = """
#     SELECT
#     json_group_array(
#         json_object(
#             'id', id,
#             'name', name,
#             'slug', slug,
#             'events', (
#                 SELECT
#                     json_group_array(
#                         json_object(
#                             'id', e.id,
#                             'name', e.name,
#                             'slug', e.slug,
#                             'active', e.active,
#                             'event_type', e.event_type,
#                             'sport', s.name,
#                             'status', e.status,
#                             'scheduled_start', e.scheduled_start,
#                             'actual_start', e.actual_start
#                         )
#                     ) AS data
#                 FROM base_event e
#                 WHERE e.sport_id = s.id
#             )
#         )
#     ) AS data
# FROM base_sport s
# """


class GetSport(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = GetSportSerializer

    @staticmethod
    def get_sport(data):
        with DBCursor() as cr:

            qry = """
            WITH tmp_sport AS (
                SELECT
                    s.id,
                    s.name,
                    s.slug,
                    s.active,
                    SUM(CASE when be.active then 1 else 0 end) AS total_event,
                    json_group_array(
                        case when be.id is not null then 
                        json_object(
                            'id', be.id,
                            'name', be.name,
                            'slug', be.slug,
                            'active', be.active,
                            'event_type', be.event_type,
                            'sport', s.name,
                            'status', be.status,
                            'scheduled_start', be.scheduled_start,
                            'actual_start', be.actual_start
                        )
                        end
                    ) AS events
                FROM
                    base_sport s
                LEFT JOIN
                    base_event be ON be.sport_id = s.id
                GROUP BY
                    s.id
            )
            SELECT *
            FROM tmp_sport
            """
            req_filters = data.get('filter')
            filters = []
            if req_filters:
                if req_filters.get('totalEvent'):
                    filters.append('total_event >= %s' % req_filters["totalEvent"])

                if req_filters.get('name'):
                    filters.append("UPPER(name) LIKE UPPER('%%%s%%')" % req_filters['name'])

                if req_filters.get('slug'):
                    filters.append("UPPER(slug) LIKE UPPER('%%%s%%')" % req_filters['slug'])

                if req_filters.get('active'):
                    filters.append("active = %s" % req_filters['active'])

            if filters:
                qry_cond = ' AND '.join(filters)
                qry = f'{qry} WHERE {qry_cond}'

            cr.execute(qry)
            rows = cr.dictfetchall()
            rows = map(lambda x: {**x, 'events': json.loads(x.get('events'))}, rows)
            resp = {
                **ErrorCodes.get_error_response(200),
                'data': rows
            }
            return resp

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({**ErrorCodes.get_error_response(500), 'responseMessage': serializer.errors})

        resp = self.get_sport(serializer.validated_data)
        return Response(resp)


class GetEvent(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def get_event(data):
        with DBCursor() as cr:
            # check if record exists in system or not
            qry = """
                WITH tmp_event AS (
                    SELECT 
                        be.id,
                        be.name,
                        be.slug,
                        be.active,
                        be.event_type,
                        be.status,
                        be.scheduled_start,
                        be.actual_start,
                        SUM(CASE when bsel.active then 1 else 0 end) total_selection,
                        json_group_array(
                            case when bsel.id is not null then 
                                json_object(
                                    'id', bsel.id,
                                    'name', bsel.name,
                                    'active', bsel.active,
                                    'price', bsel.price,
                                    'outcome', bsel.outcome
                                )
                            end
                        ) AS selections
                    FROM base_event be
                    left join base_selection bsel on be.id = bsel.event_id 
                    GROUP BY be.id 
                )
                SELECT * FROM tmp_event
            """
            req_filters = data.get('filter')
            filters = []

            if req_filters:
                if req_filters.get('totalSelection'):
                    filters.append('total_selection >= %s' % req_filters["totalSelection"])

                if req_filters.get('name'):
                    filters.append("UPPER(name) LIKE UPPER('%%%s%%')" % req_filters['name'])

                if req_filters.get('slug'):
                    filters.append("UPPER(slug) LIKE UPPER('%%%s%%')" % req_filters['slug'])

                if req_filters.get('status'):
                    filters.append("status = '%s'" % req_filters['status'])

                if req_filters.get('event_type'):
                    filters.append("event_type = '%s'" % req_filters['event_type'])

                if req_filters.get('active'):
                    filters.append("active = %s" % req_filters['active'])

                if req_filters.get('scheduled_date'):
                    '2023-06-30 23:30:00+05:30'
                    date_filter = req_filters['scheduled_date']
                    utc_scheduled_date, utc_scheduled_date_str = convert_tz(date_filter)
                    filters.append("strftime('%%Y-%%m-%%d %%H:%%M', scheduled_start) = '%s'" % utc_scheduled_date_str)
                if req_filters.get('actual_date'):
                    date_filter = req_filters['actual_date']
                    utc_actual_date, utc_actual_date_str = convert_tz(date_filter)
                    filters.append("strftime('%%Y-%%m-%%d %%H:%%M', actual_start) = '%s'" % utc_actual_date_str)

            if filters:
                qry_cond = ' AND '.join(filters)
                qry = f'{qry} WHERE {qry_cond}'

            cr.execute(qry)
            rows = cr.dictfetchall()
            rows = map(lambda x: {**x, 'selections': json.loads(x.get('selections'))}, rows)
            resp = {
                **ErrorCodes.get_error_response(200),
                'data': rows
            }
            return resp

    def post(self, request, *args, **kwargs):
        resp = self.get_event(request.data)
        return Response(resp)


class GetSelection(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def get_selection(data):
        with DBCursor() as cr:
            qry = """
                WITH tmp_selection AS (
                    SELECT 
                        sel.id,
                        sel.name,
                        sel.active,
                        sel.price,
                        sel.outcome
                    FROM
                        base_selection sel
                )
                SELECT *
                FROM tmp_selection
            """

            req_filters = data.get('filter')
            filters = []

            if req_filters:
                if req_filters.get('name'):
                    filters.append("UPPER(name) LIKE UPPER('%%%s%%')" % req_filters['name'])

                if req_filters.get('outcome'):
                    filters.append("outcome = '%s'" % req_filters['outcome'])

                if req_filters.get('price'):
                    price_filter = req_filters['price']
                    if 'lte' in price_filter:
                        filters.append("price <= %s" % price_filter['lte'])
                    elif 'gte' in price_filter:
                        filters.append("price >= %s" % price_filter['gte'])
                    elif 'eq' in price_filter:
                        filters.append("price = %s" % price_filter['eq'])

                if req_filters.get('active'):
                    filters.append("active = %s" % req_filters['active'])

            if filters:
                qry_cond = ' AND '.join(filters)
                qry = f'{qry} WHERE {qry_cond}'

            cr.execute(qry)
            rows = cr.dictfetchall()

            resp = {
                **ErrorCodes.get_error_response(200),
                'data': rows
            }
            return resp

    def post(self, request, *args, **kwargs):
        resp = self.get_selection(request.data)
        return Response(resp)
