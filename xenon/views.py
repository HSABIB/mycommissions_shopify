from django.shortcuts import render, redirect
from django.urls import reverse
from django.apps import apps
from django.template import RequestContext

from api.views import _send_store

import hmac, base64, hashlib, binascii, os
import shopify
import requests
import simplejson as JSON


def _new_session(shop_url):
    api_version = apps.get_app_config('xenon').SHOPIFY_API_VERSION
    return shopify.Session(shop_url, api_version)

def authenticate_shopify(request):
    shop_url = request.GET.get('shop', request.POST.get('shop')).strip()
    if not shop_url and ('shop' not in request.GET ):
        messages.error(request, "A shop param is required")
        return redirect(reverse(login)) # to change 
    elif 'shop' in request.GET :
        shop_url = request.GET.get('shop')
        if not shop_url :
            messages.error(request, "A shop param is required")
            return redirect(reverse(login)) # to change 
    scope = apps.get_app_config('xenon').SHOPIFY_API_SCOPE
    redirect_uri = request.build_absolute_uri(reverse(finalize))
    state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
    request.session['shopify_oauth_state_param'] = state
    permission_url = _new_session(shop_url).create_permission_url(scope, redirect_uri, state)
    return redirect(permission_url)

def finalize(request):
    api_secret = apps.get_app_config('xenon').SHOPIFY_API_SECRET
    params = request.GET.dict()

    try :
        if request.session['shopify_oauth_state_param'] != params['state']:
            messages.error(request, 'Anti-forgery state token does not match the initial request.')
        else:
            request.session.pop('shopify_oauth_state_param', None)
    except KeyError :
        print('oups')

    myhmac = params.pop('hmac')
    line = '&'.join([
        '%s=%s' % (key, value)
        for key, value in sorted(params.items())
    ])
    h = hmac.new(api_secret.encode('utf-8'), line.encode('utf-8'), hashlib.sha256)
    # 
    if hmac.compare_digest(h.hexdigest(), myhmac) == False:
        messages.error(request, "Could not verify a secure login")
        return redirect('/')

    # save shopify URL
    store_url = params['shop']
    api_version = apps.get_app_config('xenon').SHOPIFY_API_VERSION
    session = _new_session(store_url)
    access_token = session.request_token(request.GET)
    session = shopify.Session( store_url, api_version, access_token )
    shopify.ShopifyResource.activate_session(session)
    name = shopify.Shop.current().name
    response_content = _send_store(access_token, name, store_url)
    if response_content['response_code'] == 0
        print('yy')
    elif response_content['response_code'] == -1
        print('xx')
    return redirect('/confirmed')