from django.shortcuts import redirect
from douban.service import DoubanService
from douban.client import OAuthClient
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from kaike.course.models import Course
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.models import User

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

secrects ={}

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
        douban_title = people.title.text
        try:
            user = User.objects.get(username=douban_user_id)
            user.set_password(access_secret)
            user.save()
        except User.DoesNotExist:
            user=User.objects.create_user(douban_user_id,douban_title+'@douban.com',access_secret)
            user.first_name = douban_title
            user.save()
        user = auth.authenticate(username=douban_user_id,password=access_secret)
        auth.login(request, user)
        return logged(request,user)
    return redirect(CALLBACK_URL)

def logged(request,user):
    template_name='index.html'
    t = get_template(template_name)
    info={}
    info.update(csrf(request))
    info = {'course_list': Course.objects.all(),'user':user,'logged':True}
    html = t.render(Context(info))
    response = HttpResponse(html)
    return response
