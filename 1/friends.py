import os
import sys

import requests
import datetime

TOKEN = os.environ.get('TOKEN')
API_VERSION = '5.81'


def get_user_id(user_id: str):
    """Returns user_id in integer"""

    data = {
        'v': API_VERSION,
        'access_token': TOKEN,
        'user_ids': user_id
    }

    req = requests.get('https://api.vk.com/method/users.get', params=data)

    return req.json()['response'][0]['id']


def get_friends_list_by_id(user_id: str):
    """Returns list of friends by id"""

    data = {
        'v': API_VERSION,
        'access_token': TOKEN,
        'user_id': get_user_id(user_id=user_id),
        'fields': 'bdate'
    }

    req = requests.get('https://api.vk.com/method/friends.get', params=data)

    return req.json()['response']['items']


def get_birthdays():
    """Returns all birthday dates from list of friends"""
    data = get_friends_list_by_id(sys.argv[1])

    list_of_bds = list()

    for value in data:
        list_of_bds.append(value.get('bdate'))

    return list_of_bds


def check_dots(text: str):
    """Checks for valid date format"""
    return text.count('.') >= 2


def get_normal_date_formats():
    """Creates new list with valid dates"""
    data = get_birthdays()
    new_data = list()

    for value in data:
        if value is None or not check_dots(value):
            continue

        new_data.append(value)

    return new_data


def get_age_stats():
    """Return age stats by VK user_id"""
    now = datetime.datetime.now().year
    data = get_normal_date_formats()

    result = dict()

    for value in data:
        year = value.split('.')[2]
        dif = now - int(year)

        result[dif] = result.get(dif, 0) + 1

    return result


res = get_age_stats()
print(res)
