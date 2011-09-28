from django.conf.urls.defaults import *
from kaike.views import Home,logout
from django.conf import settings
from django.contrib import admin
from django.views.generic.list_detail import object_detail
from django.views.generic.list_detail import object_list
from kaike.course.models import *
from django.views.generic.simple import direct_to_template
from douban_client import douban_login

admin.autodiscover()


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    ('^$',Home),

    (r'^image/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/course/()', include(admin.site.urls)),
    (r'^course/(?P<object_id>\d+)/$', object_detail, {'template_name': 'course_details.html','queryset': Course.objects.all()}),
    (r'^lecture/(?P<object_id>\d+)/$', object_detail, {'template_name': 'lecture_details.html','queryset': Lecture.objects.all()}),
    (r'^lecture/(?P<object_id>\d+)/assignment/$', object_detail, {'template_name': 'assignment_details.html','queryset': Lecture.objects.all()}),
    (r'^lecture/(?P<object_id>\d+)/forum/$', object_detail, {'template_name': 'lecture_forum.html','queryset': Lecture.objects.all()}),
    (r'^comments/', include('django.contrib.comments.urls')),         
    ('^course/apply$',direct_to_template,{'template':'apply.html'}),
    ('^dlogin$', douban_login),
    ('^logout$', logout),

           
)
