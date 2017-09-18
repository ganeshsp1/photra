
# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    baseurl = "https://maps.googleapis.com/maps/api/geocode/json?address="
    yql_query = makeYqlQuery(req)
    print("query:")
    print(json.dumps(yql_query, indent=4))
    if yql_query is None:
        return {}
    yql_url = baseurl + yql_query
    result = urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return city

def makeWebhookResult(data):

    results = data.get('results')
    print("Results:")
    print(json.dumps(yql_query, indent=4))
    if results is None:
        return {}
        
    for result in results:
        geometry = result.get('geometry')
        if geometry is None:
            return {}
        location = geometry.get('location')
        if location is None:
            return {}
    baseurl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=AIzaSyCXLMsw0sL_TrHjtgR7DjEM3gHKb5QnJzs&radius=500"
    
    lat = location.get('lat')
    lng = location.get('lng')
    yql_url = baseurl + "&location=" + str(lat) + "," + str(lng)
    result = urlopen(yql_url).read()
    newResult = json.loads(result)
    newResults=newResult.get('results')
    if newResults is None:
        return {}
    photosList = "tets"
    #newResults = json.dumps(newResults, indent=4)
    #yql_url1 = newResults
    for d in newResults:
        photos = d.get('photos')
        for photo in photos:
            photosList = photos[ 0 ].get('photo_reference')
    baseurl = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&key=AIzaSyCXLMsw0sL_TrHjtgR7DjEM3gHKb5QnJzs&photoreference="
    yql_url1 = baseurl + str(photosList)
    return {
        "speech": "Test",
        "displayText": "Test",
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample",
         "messages": [
         {
          "type": "simple_response",
          "platform": "google",
          "textToSpeech": "Hi"
        }, {
          "type": "carousel_card",
          "platform": "google",
          "items": [
            {
              "optionInfo": {
                "key": "KEY1",
                "synonyms": []
              },
              "title": "tAJmAHAL",
              "image": {
                "url": yql_url1
              }
            },
            {
              "optionInfo": {
                "key": "KEY2",
                "synonyms": []
              },
              "title": "eFFIEL TOWER",
              "image": {
                "url": yql_url1
              }
            }
          ]
        }]
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
