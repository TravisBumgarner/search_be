from flask import Flask, Response, request
import requests
import json
from flask_cors import CORS
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch

es = Elasticsearch()

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})


@app.route("/")
def test():
    return "Ok."

@app.route("/stats")
def stats():
    es_request_body = {
        "aggs" : {
            "max_sq_ft" : { "max" : { "field" : "sq__ft" } },
            "min_sq_ft" : { "min" : { "field" : "sq__ft" } },
            "distinct_beds" : { "terms" : { "field" : "beds", "size": 100 } },
            "distinct_zips" : { "terms" : { "field" : "zip", "size": 100 } }
        }
    }
    es_response = requests.post('http://localhost:9200/housing4/_search?size=0', json=es_request_body)
    es_response = json.loads(es_response.text)

    hits = es_response['hits']['total']
    aggregations = es_response['aggregations']

    max_sq_ft = aggregations['max_sq_ft']['value']
    min_sq_ft = aggregations['min_sq_ft']['value']

    distinct_zips = aggregations['distinct_zips']['buckets']

    distinct_beds = list(map(lambda x: x['key'], aggregations['distinct_beds']['buckets']))
    distinct_beds.sort()

    be_response = Response(json.dumps({
        'distinct_zips': distinct_zips,
        'max_sq_ft': max_sq_ft,
        'min_sq_ft': min_sq_ft,
        'hits': hits,
        'distinct_beds': distinct_beds,
    }))
    be_response.headers['content-type'] = 'application/json'


    return be_response


@app.route("/search/all")
def search():
    start_from = request.args.get('start_from')
    query = request.args.get('query')
    beds = request.args.get('beds')
    baths = request.args.get('baths')

    index='housing'


    s = Search(using=es, index=index).query("match", beds=None).query("match", baths=baths)

    res = s.execute()

    # request_body = {}
    # index='housing'
    # data_type=''
    # url = 'http://localhost:9200/{}/_search/{}'.format(index, data_type)
    #
    # headers = {
    #     'content-type': 'application/json',
    # }
    #
    # res = requests.post(
    #     url,
    #     headers=headers,
    #     data=request_body
    # )
    resp = Response(json.dumps(res.to_dict()))
    resp.headers['content-type'] = 'application/json'

    return resp







