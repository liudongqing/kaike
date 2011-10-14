from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import get_template
from django.template import Context
from course.models import *
from course.forms import *
from answers.models import Question,new_question,new_answer
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.contrib import auth
import logging


def Home(request):
    course_list = Course.objects.all()
    info = {'course_list': course_list}
    info.update(csrf(request))
    if request.user.is_authenticated():
        info['user'] = request.user
        info['logged']=True
        info['reg_courses']=[x.course for x in Register.objects.filter(student=request.user)]
    t = get_template('index.html')
    html = t.render(Context(info))
    return HttpResponse(html)

def view_course(request,course_id):
    template_name='course_details.html'
    course = Course.objects.get(pk=course_id)
    info = {'course': course}
    info.update(csrf(request))
    if request.user.is_authenticated():
        info['user'] = request.user
        info['is_teacher'] = course.teacher == request.user
        info['logged']=True
        if Register.is_registered(request.user,course):
            info['registered']=True
    t = get_template(template_name)
    html = t.render(Context(info))
    return HttpResponse(html)

def edit_course(request,course_id):
    template_name='course_edit.html'
    course = Course.objects.get(pk=course_id)
    info = {'course': course}
    info.update(csrf(request))
    info['form'] = CourseForm(instance=course)
    if request.user.is_authenticated():
        info['user'] = request.user
        info['logged']=True
        if Register.is_registered(request.user,course):
            info['registered']=True
    t = get_template(template_name)
    html = t.render(Context(info))
    return HttpResponse(html)

def save_course(request,course_id):
    course = Course.objects.get(pk=course_id)
    form = CourseForm(request.POST,instance=course)
    form.save()
    return redirect('/course/%s' % course_id)

def save_lecture(request,lecture_id):
    lecture = Lecture.objects.get(pk=lecture_id)
    form = EditLectureForm(request.POST,instance=lecture)
    form.is_valid()
    logging.debug("error %s" % form.errors)
    l = form.save()
    return redirect('/lecture/%s' % l.id)

def create_lecture(request,course_id):
    form = NewLectureForm(request.POST)
    course = Course.objects.get(pk=course_id)
    lecture = form.save(commit=False)
    lecture.teacher = request.user
    lecture.course = course
    l = form.save()
    return redirect('/lecture/%s' % l.id)
    
def view_lecture(request,lecture_id):
    template_name='lecture_details.html'
    lecture = Lecture.objects.get(pk=lecture_id)
    info = {'lecture': lecture}
    info.update(csrf(request))
    if request.user.is_authenticated():
        info['user'] = request.user
        info['logged']=True
        info['is_teacher'] = request.user == lecture.teacher
    t = get_template(template_name)
    html = t.render(Context(info))
    return HttpResponse(html)

def new_lecture(request,course_id):
    template_name='lecture_edit.html'
    course = Course.objects.get(pk=course_id)
    info = {'course': course}
    info['is_new'] = True
    info.update(csrf(request))
    form = NewLectureForm()
    info['form'] = form
    if request.user.is_authenticated():
        info['user'] = request.user
        info['logged']=True
    t = get_template(template_name)
    html = t.render(Context(info))
    return HttpResponse(html)

def edit_lecture(request,lecture_id):
    template_name='lecture_edit.html'
    lecture = Lecture.objects.get(pk=lecture_id)
    info ={'lecture':lecture}
    info.update(csrf(request))
    info['form'] = EditLectureForm(instance=lecture)
    info['is_new'] = False
    if request.user.is_authenticated():
        info['user'] = request.user
        info['logged']=True
    t = get_template(template_name)
    html = t.render(Context(info))
    return HttpResponse(html)


def view_assign(request,lecture_id):
    template_name='lecture_assignment.html'
    lecture = Lecture.objects.get(pk=lecture_id)
    info = {'lecture': lecture}
    info.update(csrf(request))
    if request.user.is_authenticated():
        info['user'] = request.user
        info['logged']=True
    t = get_template(template_name)
    html = t.render(Context(info))
    return HttpResponse(html)

def reg_course(request,course_id):
    if request.user.is_authenticated():
        course = Course.objects.get(pk=course_id)
        register(request.user,course)
    return redirect('/course/'+course_id)    

def apply(request):
    template_name='apply.html'
    info = {}
    info.update(csrf(request))
    if request.user.is_authenticated():
        info['user'] = request.user
        info['logged']=True
    t = get_template(template_name)
    html = t.render(Context(info))
    return HttpResponse(html)
    
def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
    return redirect("/")
    
    
def logout(request):
    auth.logout(request)
    return redirect("/")

def dashboard(request):
    template_name='dashboard.html'
    info = {}
    info.update(csrf(request))
    if request.user.is_authenticated():
        info['user'] = request.user
        info['logged']=True
    t = get_template(template_name)
    html = t.render(Context(info))
    return HttpResponse(html)

def list_questions(request,lecture_id):
    """
    load all the questions according to the lecture id.
    """
    context = {}
    context.update(csrf(request))
    if request.user.is_authenticated():
        context['logged'] = True
        context['user'] = request.user
    try:
        lecture = Lecture.objects.get(pk=lecture_id)
        question_list = Question.objects.filter(topic=lecture.title)
        context['lecture'] = lecture
        context['question_list'] = question_list
        logging.debug(question_list)
    except Exception:
        logging.error( "query Lecture error")
    
    t = get_template('lecture_forum.html')
    html = t.render(Context(context))
    
    return HttpResponse(html)
    
def ask(request,lecture_id):
    if request.user:
         lecture = Lecture.objects.get(pk=lecture_id)
         q = new_question(request.user,title=request.POST['title'],content = request.POST['content'],topic=lecture.title)
         q.save()
    return redirect('/lecture/'+lecture_id+'/forum')    

def reply(request,lecture_id,question_id):
    if request.user:
         lecture = Lecture.objects.get(pk=lecture_id)
         question = Question.objects.get(pk=question_id)
         a = new_answer(request.user,content=request.POST['content'],question=question)
         a.save()
    return redirect('/lecture/'+lecture_id+'/forum/question/'+question_id)   

def expand_question(request,lecture_id,question_id): 
    """
    load all the questions according to the lecture id.
    """
    context = {}
    context.update(csrf(request))
    if request.user.is_authenticated():
        context['logged'] = True
        context['user'] = request.user
    try:
        lecture = Lecture.objects.get(pk=lecture_id)
        expand_question= Question.objects.get(pk=question_id)
        context['lecture'] = lecture
        context['expand_question'] = expand_question
    except Exception:
        logging.error( "query Lecture error")
    
    t = get_template('lecture_forum.html')
    html = t.render(Context(context))
    
    return HttpResponse(html)