from django.http import HttpResponse
from apps.question.models import Event
from django.views.decorators.csrf import csrf_exempt
import datetime
from random import randint


def this_weekend_definition():
    start = datetime.date.today()
    end = datetime.date.today()

    if start.weekday() < 5:
        diff = 5 - start.weekday()
        start += datetime.timedelta(diff)

    if start.weekday() == 5:
        end = start + datetime.timedelta(2)
    else:
        end = start + datetime.timedelta(1)

    return "{}T13:00:00Z".format(str(start)), "{}T07:00:00Z".format(str(end))


@csrf_exempt
def index(request):
    start, end = this_weekend_definition()
    query_set = Event.objects.filter(start__gte=start, end__lte=end)
    count = query_set.count()

    random_int = randint(0, count-1)

    event = query_set[random_int:random_int+1][0]
    return HttpResponse("Upcoming Event: {}, {}".format(event.name, event.start))

