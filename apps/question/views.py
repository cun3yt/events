from django.http import HttpResponse
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from apps.question.models import Event
import datetime
from random import randint
import time


def this_weekend_definition():
    start = datetime.date.today()

    if start.weekday() < 5:
        diff = 5 - start.weekday()
        start += datetime.timedelta(diff)

    end = start + (datetime.timedelta(2) if start.weekday() == 5 else datetime.timedelta(1))
    return "{}T13:00:00Z".format(str(start)), "{}T07:00:00Z".format(str(end))


@csrf_exempt
def random_weekend_event(request):
    start, end = this_weekend_definition()
    query_set = Event.objects.filter(start__gte=start, end__lte=end)
    count = query_set.count()

    random_int = randint(0, count-1)
    event = query_set[random_int:random_int+1][0]

    url = "http://{}{}?id={}".format(request.get_host(), reverse('event_details'), event.event_id)
    return JsonResponse({
        "text": "I found a great event for you. I hope you like it!\n*<{}|{}>*".format(url, event.name),
        "username": "Events Bot",
        "mrkdwn": True,
        "attachments": [
            {
                "pretext": (event.description[:140] + '...') if len(event.description) > 140 else event.description,
                "title": event.name,
                "fallback": "Required plain-text summary of the attachment.",
                "color": "#36a64f",
                "title_link": url,
                "text": (event.description[:140] + '...') if len(event.description) > 140 else event.description,
                "fields": [],
                "image_url": event.logo,
                "thumb_url": event.logo,
                "footer": "Weekend Fun",
                # "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
                "ts": int(time.mktime(event.start.timetuple()))
            }
        ]
    })


def event_details(request):
    event_id = request.GET.get('id')
    event = Event.objects.filter(event_id=event_id).get()
    return HttpResponse(
        "<p>{}</p><p>{}</p><img src='{}'>".format(event.name, event.description, event.logo)
    )
