from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='conference_home'),
    path('about/', about, name='conference_about'),
    path('welcome/<str:name>', welcome, name='conference_welcome'),
    path('list/', listConferences, name='conference_list'),
    path('listLV/', ConferenceListView.as_view(), name='conference_listLV'),
    path('details/<int:pk>/', ConferenceDetailView.as_view(), name='conference_details'),
    path('create/', ConferenceCreateView.as_view(), name='conference_create'),
    path('update/<int:pk>/', ConferenceUpdateView.as_view(), name='conference_update'),
]