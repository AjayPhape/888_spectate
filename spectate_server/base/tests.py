from django.db import transaction
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class TestCreateAPI(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_sport(self):
        request_data = {
            'name': 'BaseBall',
            'slug': 'BaseBallSlug',
            'active': 'true'
        }

        url = reverse('base:create_sport')
        response = self.client.post(url, request_data, format='json')

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data['responseCode'] == 200
        assert 'id' in response_data
        assert isinstance(response_data['id'], int)
        return response_data

    def test_event(self):
        response_data = self.test_sport()

        request_data = {
            'name': 'BaseBall Match 3',
            'slug': 'BaseBall-match-3',
            'active': True,
            'event_type': 'preplay',
            'sport_id': response_data['id'],
            'status': 'pending',
            'scheduled_start': '2023-06-30 19:30:00',
            'actual_start': '2023-06-30 19:30:00'
        }

        url = reverse('base:create_event')
        response = self.client.post(url, request_data, format='json')

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()

        assert response_data['responseCode'] == 200
        assert 'id' in response_data
        assert isinstance(response_data['id'], int)
        return response_data

    def test_selection(self):
        self.test_sport()
        response_data = self.test_event()

        request_data = {
            'name': 'Base Ball Team A',
            'event_id': response_data['id'],
            'price': 1.5,
            'active': True,
            'outcome': 'unsettled'
        }

        # Make the request
        url = reverse('base:create_selection')
        response = self.client.post(url, request_data, format='json')

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data['responseCode'] == 200
        assert 'id' in response_data
        assert isinstance(response_data['id'], int)


class TestGetAPI(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_sport(self):
        # Create a sample request data
        request_data = {
            'filter': {
                'totalEvent': 5,
                'name': ''
            }
        }

        url = reverse('base:get_sport')
        response = self.client.post(url, request_data, format='json')

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert 'data' in response_data
        assert isinstance(response_data['data'], list)

    def test_event(self):
        request_data = {
            'filter': {
                'totalSelection': 0,
                'name': 'Foose',
                'scheduled_date': '2023-06-30 23:30:00+05:30'
            }
        }

        url = reverse('base:get_event')
        response = self.client.post(url, request_data, format='json')

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()

        assert response_data['responseCode'] == 200
        assert 'data' in response_data

    def test_selection(self):
        request_data = {
            'filter': {
                'name': ''
            }
        }

        # Make the request
        url = reverse('base:get_selection')
        response = self.client.post(url, request_data, format='json')

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()

        assert response_data['responseCode'] == 200
        assert 'data' in response_data


class TestUpdateAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        create_api = TestCreateAPI()
        create_api.setUp()
        create_api.test_sport()
        create_api.test_event()
        create_api.test_selection()

    def test_sport(self):
        # Create a sample request data
        request_data = {
            "id": "1",
            "name": "Foot-ball",
            "slug": "Foot-ball-Slug",
            "active": True
        }

        url = reverse('base:update_sport')
        response = self.client.post(url, request_data, format='json')

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()

        assert response_data['responseCode'] == 200

    def test_event(self):
        request_data = {
            "name": "Football Match",
            "slug": "football-match",
            "active": False,
            "event_type": "preplay",
            "id": 1,
            "status": "started",
            "scheduled_start": "2023-06-30 18:00:00",
            "actual_start": None
        }

        url = reverse('base:update_event')
        response = self.client.post(url, request_data, format='json')

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()

        assert response_data['responseCode'] == 200

    def test_selection(self):
        request_data = {
            "name": "Basketball Team B",
            "id": 1,
            "price": 1.5,
            "active": True,
            "outcome": "unsettled"
        }

        # Make the request
        url = reverse('base:update_selection')
        response = self.client.post(url, request_data, format='json')

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()

        assert response_data['responseCode'] == 200
