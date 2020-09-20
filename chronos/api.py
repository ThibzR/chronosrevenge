from django.conf import settings
import requests


def get_response(url):
    full_url = settings.CHRONOS_API_URL + url
    headers = {
        'Auth-Token': settings.CHRONOS_API_TOKEN,
        'Cache-Control': '60'
        }
    return requests.get(full_url, headers=headers)