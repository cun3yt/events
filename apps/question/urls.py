from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^fun-event$', views.random_weekend_event, name='random_weekend_event'),
    url(r'^fun-event-response$', views.fun_event_user_action, name='random_weekend_user_action'),
    url(r'^$', views.event_details, name='event_details'),
]
