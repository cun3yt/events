from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^fun-event$', views.index, name='index'),
]
