from django.shortcuts import render

import requests
import simplejson as JSON


ENDPOINT_URL = 'http://localhost:8001/'
ENDPOINT_ROUTE = 'get-store/'

def _send_store(api_token, name, url) :
    try :
        url = ENDPOINT_URL + ENDPOINT_ROUTE
        post_data = {
            'api_token' : api_token,
            'name' : name,
            'url': url
        }
        response = requests.post(url, post_data)
        content = JSON.loads( response.content.decode() )
        return content
    except:
        return False 
