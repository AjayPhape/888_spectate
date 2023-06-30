from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import pytest


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestGetAPI:
    def test_sport(self, api_client):
        # Create a sample request data
        request_data = {
            "filter": {
                "totalEvent": 5,
                "name": ""
            }
        }

        url = reverse('base:get_sport')
        response = api_client.post(url, request_data, format="json")

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert "data" in response_data
        assert isinstance(response_data["data"], list)

    def test_event(self, api_client):
        request_data = {
            "filter": {
                "totalSelection": 0,
                "name": "Foose",
                "scheduled_date": "2023-06-30 23:30:00+05:30"
            }
        }

        url = reverse('base:get_event')
        response = api_client.post(url, request_data, format="json")

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()

        assert response_data["responseCode"] == 200
        assert response_data["responseMessage"] == "Success"
        assert "data" in response_data

    def test_selection(self, api_client):
        request_data = {
            "filter": {
                "name": ""
            }
        }

        # Make the request
        url = reverse('base:get_selection')
        response = api_client.post(url, request_data, format="json")

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()

        assert response_data["responseCode"] == 200
        assert response_data["responseMessage"] == "Success"
        assert "data" in response_data
