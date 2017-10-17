from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^fun-event$', views.random_weekend_event, name='random_weekend_event'),
    url(r'^$', views.event_details, name='event_details'),
]
