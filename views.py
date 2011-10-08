from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import get_template
from django.template import Context
from kaike.course.models import Course,User,Lecture
from kaike.answers.models import Question,new_question,new_answer
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

def view_course(request,course_id):
    template_name='course_details.html'
    course = Course.objects.get(pk=course_id)
    info = {'course': course}
    if request.user.is_authenticated():
        info['user'] = request.user
        info['logged']=True
    t = get_template(template_name)
    html = t.render(Context(info))
    return HttpResponse(html)

def view_lecture(request,lecture_id):
    template_name='lecture_details.html'
    lecture = Lecture.objects.get(pk=lecture_id)
    info = {'lecture': lecture}
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
    if request.user.is_authenticated():
        info['user'] = request.user
        info['logged']=True
    t = get_template(template_name)
    html = t.render(Context(info))
    return HttpResponse(html)


def apply(request):
    template_name='apply.html'
    info = {}
    if request.user.is_authenticated():
        info['user'] = request.user
        info['logged']=True
    t = get_template(template_name)
    html = t.render(Context(info))
    return HttpResponse(html)

def logout(request):
    auth.logout(request)
    return Home(request)

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
        print question_list
    except Exception as e:
        print e
    
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
    except Exception as e:
        print e
    
    t = get_template('lecture_forum.html')
    html = t.render(Context(context))
    
    return HttpResponse(html)