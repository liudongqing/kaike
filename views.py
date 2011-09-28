from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from kaike.course.models import Course,User
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.contrib import auth


def Home(request):
    course_list = Course.objects.all()
    info = {'course_list': course_list}
    if request.user.is_authenticated():
        info['user'] = request.user
        info['logged']=True
    t = get_template('index.html')
    html = t.render(Context(info))
    return HttpResponse(html)

def logout(request):
    auth.logout(request)
    return Home(request)

