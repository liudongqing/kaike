"""
The MIT License

Copyright (c) 2007 Leah Culver

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Example consumer. This is not recommended for production.
Instead, you'll want to create your own subclass of OAuthClient
or find one that works with your web framework.
"""

import httplib
import time
import oauth.oauth as oauth
from django.shortcuts import redirect
import urlparse
from douban.service import DoubanService
from douban.client import OAuthClient
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from kaike.course.models import Course,User
from django.core.context_processors import csrf
from django.shortcuts import render_to_response

# settings for the local test consumer
SERVER = 'www.douban.com'
PORT = 80

# fake urls for the test server (matches ones in server.py)
REQUEST_TOKEN_URL = 'http://www.douban.com/service/auth/request_token'
ACCESS_TOKEN_URL = 'http://www.douban.com/service/auth/access_token'
AUTHORIZATION_URL = 'http://www.douban.com/service/auth/authorize'
CALLBACK_URL = 'http://localhost:8000'
RESOURCE_URL = 'http://api.douban.com/people/'

# key and secret granted by the service provider for this consumer application - same as the MockOAuthDataStore
CONSUMER_KEY = '0e1863190be71cbc2a49294b23b55634'
CONSUMER_SECRET = '41138d1790fb5fbc'

tokens = {}
secrects ={}

# example client using httplib with headers
class DoubanOAuthClient(oauth.OAuthClient):

    def __init__(self, server, port=httplib.HTTP_PORT, request_token_url='', access_token_url='', authorization_url=''):
        self.server = server
        self.port = port
        self.request_token_url = request_token_url
        self.access_token_url = access_token_url
        self.authorization_url = authorization_url
        self.connection = httplib.HTTPConnection("%s:%d" % (self.server, self.port))
        self.douban_user_id = ''
        self.consumer = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
        self.signature_method_hmac_sha1 = oauth.OAuthSignatureMethod_HMAC_SHA1()

    def fetch_request_token(self):
        # via headers
        # -> OAuthToken
        # get request token
        print '* Obtain a request token ...'
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, callback=CALLBACK_URL, http_url=self.request_token_url)
        oauth_request.sign_request(self.signature_method_hmac_sha1, self.consumer, None)
        print 'REQUEST (via headers)'
        print 'parameters: %s' % str(oauth_request.parameters)  
        self.connection.request(oauth_request.http_method, self.request_token_url, headers=oauth_request.to_header()) 
        print oauth_request.to_header()
        response = self.connection.getresponse()
        return oauth.OAuthToken.from_string(response.read())

    def fetch_access_token(self, request_token):
        # get access token via headers
        # -> OAuthToken
        print '* Obtain an access token ...'
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=request_token, http_url=self.access_token_url)
        oauth_request.sign_request(self.signature_method_hmac_sha1, self.consumer, request_token)
        print 'REQUEST (via headers)'
        print 'parameters: %s' % str(oauth_request.parameters)
       
        self.connection.request(oauth_request.http_method, self.access_token_url, headers=oauth_request.to_header()) 
        response = self.connection.getresponse()
        response_str = response.read()
        self.douban_user_id = urlparse.parse_qs(response_str)['douban_user_id'][0]
        return oauth.OAuthToken.from_string(response_str)

    def authorize_token(self, oauth_request):
        # via url
        # -> typically just some okay response
        self.connection.request(oauth_request.http_method, oauth_request.to_url()) 
        response = self.connection.getresponse()
        print response.getheaders()
        return response.read()

    def get_douban_user_info(self, access_token):
        # via get 
        # -> douban title
        url = RESOURCE_URL+self.douban_user_id
        print '* Access protected resources ...'
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=access_token, http_method='GET', http_url=url, parameters={})
        oauth_request.sign_request(self.signature_method_hmac_sha1, self.consumer, access_token)
        print 'REQUEST (via get)'
        print 'parameters: %s' % str(oauth_request.parameters)
        headers = {'Content-Type' :'application/x-www-form-urlencoded'}
        self.connection.request('GET', url, headers=oauth_request.to_header())
        response = self.connection.getresponse()
        html = response.read()
        print html
        return html


def douban_login_old(request):
    # setup
    print '** OAuth Python Library Example **'
    client = DoubanOAuthClient(SERVER, PORT, REQUEST_TOKEN_URL, ACCESS_TOKEN_URL, AUTHORIZATION_URL)
  
    #alread authorized
    if 'oauth_token' in request.GET :
        token = tokens[request.GET['oauth_token']]
        token = client.fetch_access_token(token)
        print 'GOT'
        print 'key: %s' % str(token.key)
        print 'secret: %s' % str(token.secret)
        params = client.get_douban_user_info(token)
        print 'GOT'
        print 'non-oauth parameters: %s' % params
        return redirect(CALLBACK_URL)
        
    token = client.fetch_request_token()
    print 'GOT'
    print 'key: %s' % str(token.key)
    print 'secret: %s' % str(token.secret)
    tokens[token.key]=token
    print 'callback confirmed? %s' % str(token.callback_confirmed)
    print '* Authorize the request token ...'
    
    return redirect(client.authorization_url+'?oauth_token='+token.key+'&oauth_callback=http%3A%2F%2Flocalhost%3A8000/dlogin')

def douban_login(request):        
    client = OAuthClient(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    access_key = request.session.get('access_key')
    access_secret = request.session.get(access_key)
    douban_user_id = request.session.get('douban_user_id')
    
    if not access_key or not access_secret:
        request_key = request.GET.get('oauth_token')
        request_secret = secrects.get(request_key)
        if request_key and request_secret:
            try:
                print "try to get access token"
                access_key, access_secret, douban_user_id = client.get_access_token(request_key, request_secret) 
                print "douban id is : "+douban_user_id
                if access_key and access_secret:
                    # store user access key in cookie, 
                    # not accessable by other people
                    request.session['access_key'] = access_key
                    request.session[access_key] = access_secret
                    request.session['douban_user_id'] = douban_user_id
            except Exception:
                    access_token = None
                    print 'failed'
                    return redirect(CALLBACK_URL)
        else:
            print "try to get request token"
            client = OAuthClient(key=CONSUMER_KEY, secret=CONSUMER_SECRET) 
            key, secret = client.get_request_token()
            if key and secret:
                secrects[key] = secret
                url = client.get_authorization_url(key, secret, callback=CALLBACK_URL+"/dlogin")
                return redirect(url)
            else:
                print 'failed'
                return redirect(CALLBACK_URL)
            
    print "start to get user information"
    service = DoubanService(api_key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    if service.ProgrammaticLogin(access_key, access_secret):
        people = service.GetPeople('/people/'+douban_user_id)
        username = people.title.text
        user = User.objects.get(name=username)
        template_name='index.html' 
        t = get_template(template_name)
        info={}
        info.update(csrf(request))
        info = {'course_list': Course.objects.all(),'user':user,'logged':True}
        html = t.render(Context(info))
        response = HttpResponse(html)

        if not user:
            User.object.create_user(user)
        response.set_cookie('user.id',user.id)
        response.set_cookie('max_age',3600*24*3)
        return response
    return redirect(CALLBACK_URL)