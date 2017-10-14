import os
import requests
import traceback
import sys
from apps.question.models import Event


class EventbriteCredentials:
    @classmethod
    def get_client_secret(cls):
        env_var = 'EVENTBRITE_CLIENT_SECRET'
        return cls.__get_env_var(env_var)

    @classmethod
    def get_personal_token(cls):
        env_var = 'EVENTBRITE_PERSONAL_TOKEN'
        return cls.__get_env_var(env_var)

    @classmethod
    def get_anonymous_token(cls):
        env_var = 'EVENTBRITE_ANONYMOUS_TOKEN'
        return cls.__get_env_var(env_var)

    @classmethod
    def __get_env_var(cls, env_var):
        val = os.environ.get(env_var)
        if not val:
            raise Exception("Environment variable {} is not set".format(env_var))
        return val


def get_events(token, location, start_date_start, start_date_end, page):
    response = requests.get(
        "https://www.eventbriteapi.com/v3/events/search/",
        headers={
            "Authorization": "Bearer {}".format(token),
        },
        params={
            "location.address": location,
            "start_date.range_start": start_date_start,
            "start_date.range_end": start_date_end,
            "page": page,
        },
    )
    return response.json()


def fetch_and_save_events(location, start_date_start, start_date_end):
    token = EventbriteCredentials.get_personal_token()
    page = 1

    while True:
        print("Fetching page no: {} for location: {}".format(page, location))
        res = get_events(token=token, location=location, start_date_start=start_date_start,
                         start_date_end=start_date_end, page=page)

        print(" Total # pages: {} and current page count: {}".format(res['pagination']['page_count'],
                                                                     len(res['events'])))

        for event in res['events']:
            try:
                Event.objects.update_or_create(
                    event_id=event['id'],
                    defaults={
                        'location': location,
                        'name': event['name']['text'],
                        'description': (event.get('description') or {}).get('text', ''),
                        'start': event['start']['utc'],
                        'end': event['end']['utc'],
                        'logo': (event.get('logo') or {}).get('url', ''),
                        'url': event.get('url'),
                    }
                )
            except Exception as e:
                print("Opss! {}".format(format(e)))
                traceback.print_exc(file=sys.stdout)
                pass

        page += 1
        if res['pagination']['page_count'] < page:
            break
