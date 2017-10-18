from django.http import HttpResponse
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from apps.question.models import Event
import datetime
from random import randint
import time
import requests
from urllib.parse import parse_qsl
import json


def this_weekend_definition():
    start = datetime.date.today()

    if start.weekday() < 5:
        diff = 5 - start.weekday()
        start += datetime.timedelta(diff)

    end = start + (datetime.timedelta(2) if start.weekday() == 5 else datetime.timedelta(1))
    return "{}T13:00:00Z".format(str(start)), "{}T07:00:00Z".format(str(end))


def fetch_event(host, id=None):
    if id is None:
        start, end = this_weekend_definition()
        query_set = Event.objects.filter(start__gte=start, end__lte=end, is_published=True)
        count = query_set.count()
        random_int = randint(0, count-1)
        event = query_set[random_int:random_int+1][0]
    else:
        event = Event.objects.get(id)

    url = "http://{}{}?id={}".format(host, reverse('event_details'), event.event_id)
    return JsonResponse({
        "text": "I found a great event for you. I hope you like it!\n*<{}|{}>*".format(url, event.name),
        "username": "Events Bot",
        "mrkdwn": True,
        "replace_original": False,
        "attachments": [
            {
                "pretext": (event.description[:140] + "... [<{}|Read More>]".format(url)) if len(event.description) > 140 else event.description,
                "title": event.name,
                "fallback": "Required plain-text summary of the attachment.",
                "color": "#36a64f",
                "title_link": url,
                "text": (event.description[:140] + "... [<{}|Read More>]".format(url)) if len(event.description) > 140 else event.description,
                "fields": [],
                "image_url": event.logo,
                "thumb_url": event.logo,
                "footer": "Weekend Fun",
                # "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
                "ts": int(time.mktime(event.start.timetuple())),
                "callback_id": 'fun_weekend',
                "actions": [
                    {
                        "name": "event_response",
                        "text": "Event Details",
                        "type": "button",
                        "value": "details:{}".format(event.event_id)
                    },
                    {
                        "name": "event_response",
                        "text": "See Another Event",
                        "type": "button",
                        "value": "another_event"
                    }
                ]
            }
        ]
    })


@csrf_exempt
def random_weekend_event(request):
    response = fetch_event(request.get_host())
    return response


@csrf_exempt
def fun_event_user_action(request):
    req = json.loads(parse_qsl(request.body.decode("utf-8"))[0][1])

    action_list = req['actions'][0]['value'].split(":")
    if action_list[0] == "details":
        url = "http://{}{}?id={}".format(request.get_host(), reverse('event_details'), action_list[1])
        response_json = {
            "text": "See the details of event here: {}".format(url),
            "replace_original": False
        }
    elif action_list[0] == "another_event":
        return fetch_event(request.get_host())

    requests.post(
        req['response_url'],
        json=response_json
    )

    return HttpResponse("")


def event_details(request):
    event_id = request.GET.get('id')
    event = Event.objects.filter(event_id=event_id).get()
    return HttpResponse(
        "<p>{}</p><p>{}</p><img src='{}'>".format(event.name, event.description, event.logo)
    )
