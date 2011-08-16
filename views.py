from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from kaike.course.models import Course

def Home(request):
    course_list = Course.objects.all()
    t = get_template('index.html')
    html = t.render(Context({'course_list': course_list}))
    return HttpResponse(html)
