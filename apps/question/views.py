from django.http import HttpResponse
# from django.shortcuts import render
from apps.question.models import Event
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    event = Event.objects.all()[:1][0]
    return HttpResponse("Upcoming Event: <a href='http://www.google.com'>{}</a>".format(event.name))

