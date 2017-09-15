
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
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    baseurl = "https://maps.googleapis.com/maps/api/geocode/json?address="
    yql_query = makeYqlQuery(req)
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

    result = data.get('results')
    if result is None:
        return {}

    geometry = result.get('geometry')
    if geometry is None:
        return {}
		
	location = geometry.get('location')
    if location is None:
        return {}
	
	
	baseurl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=AIzaSyCXLMsw0sL_TrHjtgR7DjEM3gHKb5QnJzs&radius=500"

   
    yql_url = baseurl + '&location='+location.get('lat')+','+location.get('lng')
    newResult = urlopen(yql_url).read()
	
	newResults=newResult.get('results')
	   if newResults is None:
        return {}
	for d in newResults:

	geometry = newResults.get('geometry')
    if geometry is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
             ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)

    return {
        "speech": yql_url,
        "displayText": speech,
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
                "url": "http://webneel.com/daily/sites/default/files/images/daily/04-2014/4-taj-mahal-photos.preview.jpg"
              }
            },
            {
              "optionInfo": {
                "key": "KEY2",
                "synonyms": []
              },
              "title": "eFFIEL TOWER",
              "image": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Tour_Eiffel_Wikimedia_Commons_%28cropped%29.jpg/1200px-Tour_Eiffel_Wikimedia_Commons_%28cropped%29.jpg"
              }
            }
          ]
        }]
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
