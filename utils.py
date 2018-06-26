import json
import requests


def make_url(index, data_type=''):
    return 'http://localhost:9200/{}/_search/{}'.format(index, data_type)


def perform_search(data):
    url = make_url(index='housing')
    headers = {
        'content-type': 'application/json',
    }
    res = requests.post(
        url,
        headers=headers,
        data=data
    )
    return res.text