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

# settings for the local test consumer
SERVER = 'www.douban.com'
PORT = 80

# fake urls for the test server (matches ones in server.py)
REQUEST_TOKEN_URL = 'http://www.douban.com/service/auth/request_token'
ACCESS_TOKEN_URL = 'http://www.douban.com/service/auth/access_token'
AUTHORIZATION_URL = 'http://www.douban.com/service/auth/authorize'
CALLBACK_URL = 'http://localhost:8000'
RESOURCE_URL = 'http://photos.example.net/photos'

# key and secret granted by the service provider for this consumer application - same as the MockOAuthDataStore
CONSUMER_KEY = '0e1863190be71cbc2a49294b23b55634'
CONSUMER_SECRET = '41138d1790fb5fbc'

tokens = {}

# example client using httplib with headers
class DoubanOAuthClient(oauth.OAuthClient):

    def __init__(self, server, port=httplib.HTTP_PORT, request_token_url='', access_token_url='', authorization_url=''):
        self.server = server
        self.port = port
        self.request_token_url = request_token_url
        self.access_token_url = access_token_url
        self.authorization_url = authorization_url
        self.connection = httplib.HTTPConnection("%s:%d" % (self.server, self.port))

    def fetch_request_token(self, oauth_request):
        # via headers
        # -> OAuthToken
        self.connection.request(oauth_request.http_method, self.request_token_url, headers=oauth_request.to_header()) 
        print oauth_request.to_header()
        response = self.connection.getresponse()
        return oauth.OAuthToken.from_string(response.read())

    def fetch_access_token(self, oauth_request):
        # via headers
        # -> OAuthToken
        self.connection.request(oauth_request.http_method, self.access_token_url, headers=oauth_request.to_header()) 
        response = self.connection.getresponse()
        html = response.read()
        print 'response is :'+ html
        return oauth.OAuthToken.from_string(html)

    def authorize_token(self, oauth_request):
        # via url
        # -> typically just some okay response
        self.connection.request(oauth_request.http_method, oauth_request.to_url()) 
        response = self.connection.getresponse()
        print response.getheaders()
        return response.read()

    def access_resource(self, oauth_request):
        # via post body
        # -> some protected resources
        headers = {'Content-Type' :'application/x-www-form-urlencoded'}
        self.connection.request('POST', RESOURCE_URL, body=oauth_request.to_postdata(), headers=headers)
        response = self.connection.getresponse()
        return response.read()


def douban_login(request):
    # setup
    print '** OAuth Python Library Example **'
    client = DoubanOAuthClient(SERVER, PORT, REQUEST_TOKEN_URL, ACCESS_TOKEN_URL, AUTHORIZATION_URL)
    consumer = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
    signature_method_hmac_sha1 = oauth.OAuthSignatureMethod_HMAC_SHA1()
    
    #alread authorized
    if 'oauth_token' in request.GET :
        # get access token
        print '* Obtain an access token ...'
        token = tokens[request.GET['oauth_token']]
        print ' Token is ', token
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer, token=token, http_url=client.access_token_url)
        oauth_request.sign_request(signature_method_hmac_sha1, consumer, token)
        print 'REQUEST (via headers)'
        print 'parameters: %s' % str(oauth_request.parameters)
        token = client.fetch_access_token(oauth_request)
        print 'GOT'
        print 'key: %s' % str(token.key)
        print 'secret: %s' % str(token.secret)
        
        return redirect(CALLBACK_URL)
        
    # get request token
    print '* Obtain a request token ...'
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer, callback=CALLBACK_URL, http_url=client.request_token_url)
    oauth_request.sign_request(signature_method_hmac_sha1, consumer, None)
    print 'REQUEST (via headers)'
    print 'parameters: %s' % str(oauth_request.parameters)
    token = client.fetch_request_token(oauth_request)
    print 'GOT'
    print 'key: %s' % str(token.key)
    print 'secret: %s' % str(token.secret)
    tokens[token.key]=token
    print 'callback confirmed? %s' % str(token.callback_confirmed)

    print '* Authorize the request token ...'
    
    return redirect(client.authorization_url+'?oauth_token='+token.key+'&oauth_callback=http%3A%2F%2Flocalhost%3A8000/dlogin')
    