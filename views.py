from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from kaike.course.models import Course,User
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from oauth import oauth


def Home(request):
    course_list = Course.objects.all()
    info = {'course_list': course_list}
    if request.session.has_key('user.id'):
        user_id = request.session['user.id']
        info['user'] = User.objects.get(pk=int(user_id))
        info['logged']=True
    t = get_template('index.html')
    html = t.render(Context(info))
    return HttpResponse(html)


def login(request):
    info={}
    info.update(csrf(request))
    user = None 
    template_name = 'login.html'
    if request.POST.has_key('name'):
        course_list = Course.objects.all()
        user = User.objects.get(name=request.POST['name'])
        request.session['user.id']= user.id
        info = {'course_list': course_list,'user':user,'logged':True}
        template_name='index.html' 
    t = get_template(template_name)
    html = t.render(Context(info))
    response = HttpResponse(html)
    if user:
        response.set_cookie('user.id',user.id)
        response.set_cookie('max_age',3600*24*3)
    return response

def logout(request):
    if request.session.has_key('user.id'):
        del request.session['user.id']
    return Home(request)

