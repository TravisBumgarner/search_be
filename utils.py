import json
import requests


def make_url(index, data_type=''):
    return 'http://localhost:9200/{}/_search/{}'.format(index, data_type)


def perform_search(start_from):
    query_dict = {
        "query": {
            "match_all": {}
        }
    }
    query_str = json.dumps(query_dict)
    url = make_url(index='people2')
    headers = {
        'content-type': 'application/json',
    }
    params = {
        'size': 5,
        'from': start_from,
    }
    res = requests.get(
        url,
        data=query_str,
        headers=headers,
        params=params
    )
    return res.text