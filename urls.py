from django.conf.urls.defaults import *
from kaike.views import *
from django.conf import settings
from django.contrib import admin
from django.views.generic.list_detail import object_detail
from django.views.generic.list_detail import object_list
from kaike.course.models import *
from django.views.generic.simple import direct_to_template
from douban_client import douban_login



# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    ('^$',Home),
    ('^mine$',dashboard),

    (r'^image/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT+"/image/"}),
    (r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT+"/css/"}),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/course/()', include(admin.site.urls)),
    (r'^course/(?P<course_id>\d+)/$', view_course),
    (r'^course/(?P<course_id>\d+)/register/$', reg_course),
    (r'^lecture/(?P<lecture_id>\d+)/$', view_lecture),
    (r'^lecture/(?P<lecture_id>\d+)/assignment/$', view_assign),
    (r'^lecture/(?P<lecture_id>\d+)/forum/$', list_questions),
    (r'^lecture/(?P<lecture_id>\d+)/forum/ask$', ask),
    (r'^lecture/(?P<lecture_id>\d+)/forum/question/(?P<question_id>\d+)/$', expand_question),
    (r'^lecture/(?P<lecture_id>\d+)/forum/question/(?P<question_id>\d+)/reply$', reply),
    ('^course/apply$',apply),
    ('^dlogin$', douban_login),
    ('^logout$', logout),

           
)
