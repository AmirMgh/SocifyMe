from flask import Flask, request, Response, make_response, current_app
import json
from bson.json_util import dumps
import crawl_people as ppl_crawler
import database
from datetime import timedelta
from functools import update_wrapper
from twitter_crawler import TwitterCrawlerAPI

app = Flask(__name__)
db = database.connect_to_mong()

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

#@app.route('/1.0/tweets', methods = ['POST'])
#@crossdomain(origin='*')
#def api_tweets():
#    if request.headers['Content-Type'] == 'application/json':
#        hashtag = request.json['hashtag']
#        written_tw = 11#ppl_crawler.collect_tweets(hashtag, db)
#        js = json.dumps({'tweets_no' : written_tw})
#        response = Response(js, status=200, mimetype='application/json')
        #response.headers['Access-Control-Allow-Origin'] = "*"
        #return "JSON Message: " + json.dumps({'tweets_no' : written_tw})
#        return response
#    else:
#        return "415 Unsupported Media Type ;)"

@app.route('/1.0/tweets')
@crossdomain(origin='*')
def api_tweets():
    hashtag = request.args['hashtag']
    tw_handle = request.args['tw_handle']
    twitterAPI = TwitterCrawlerAPI()
    result = twitterAPI.runCrawler(tw_handle, db)
    if result:
        #find and store people nearby
        ppl_no = ppl_crawler.collect_tweets(hashtag, db)
        js = json.dumps({'people_no' : ppl_no})
    else:
        js = json.dumps({'people_no' : -1})
    response = Response(js, status=200, mimetype='application/json')
    return response

@app.route('/1.0/people')
@crossdomain(origin='*')
def api_people():
    if 'rank' in request.args:
        return 'ranking based on ' + request.args['rank']
    #get all users from db
    users = db.users.find()
    js = dumps(users)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
