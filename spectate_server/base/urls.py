from django.urls import path

from base.create_views import CreateEvent, CreateSport, CreateSelection
from base.update_views import UpdateSport, UpdateEvent, UpdateSelection
from base.views import GetSport, GetEvent, GetSelection

app_name = 'base'

urlpatterns = [
    path('createSport/', CreateSport.as_view(), name='create_sport'),
    path('createEvent/', CreateEvent.as_view(), name='create_event'),
    path('createSelection/', CreateSelection.as_view(), name='create_selection'),

    path('updateSport/', UpdateSport.as_view(), name='update_sport'),
    path('updateEvent/', UpdateEvent.as_view(), name='update_event'),
    path('updateSelection/', UpdateSelection.as_view(), name='update_selection'),

    path('getSport/', GetSport.as_view(), name='get_sport'),
    path('getEvent/', GetEvent.as_view(), name='get_event'),
    path('getSelection/', GetSelection.as_view(), name='get_selection'),
]
