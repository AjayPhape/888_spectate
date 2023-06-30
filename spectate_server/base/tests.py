# import pytest as pytest
# from django.test import TestCase
#
# # Create your tests here.
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient
#
# def test_get_sport(api_client):
#     url = reverse('get-sport')  # Replace with your URL name or pattern
#     data = {
#         'filter': {
#             'totalEvent': 10,
#             'name': 'football'
#         }
#     }
#
#     # Make a POST request to the API endpoint
#     response = api_client.post(url, data, format='json')
#
#     # Assert the response status code and any other relevant assertions
#     assert response.status_code == status.HTTP_200_OK
#     assert 'data' in response.data
#     assert len(response.data['data']) > 0
#     assert response.data['data'][0]['name'] == 'Football'
#
# # Test setup
# @pytest.fixture
# def api_client():
#     return APIClient()
#
# # Register the test case with pytest
# @pytest.mark.django_db
# def test_get_sport(api_client):
#     # Call the actual test function
#     test_get_sport(api_client)
#
#
#
# import json
# from rest_framework import status
# from rest_framework.test import APIRequestFactory, APIClient
# import pytest
#
# from your_app.views import GetSport
#
# @pytest.fixture
# def api_client():
#     return APIClient()
#
# @pytest.fixture
# def api_factory():
#     return APIRequestFactory()
#
# @pytest.mark.django_db
# def test_get_sport(api_factory, api_client):
#     # Create a sample request data
#     request_data = {
#         "filter": {
#             "totalEvent": 5,
#             "name": "example"
#         }
#     }
#
#     # Create a request using the API factory
#     url = "/path/to/get_sport/"
#     request = api_factory.post(url, request_data, format="json")
#
#     # Use the API client to send the request
#     response = api_client.post(url, request_data, format="json")
#
#     assert response.status_code == status.HTTP_200_OK
#
#     # Parse the response JSON and assert its contents
#     response_data = response.json()
#     assert "data" in response_data
#     assert isinstance(response_data["data"], list)
#
#     # Add more assertions as needed
#
