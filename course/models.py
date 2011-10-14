# -*- coding: utf-8 -*
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    website = models.URLField()

    def __unicode__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=100,verbose_name=u'课名')
    introduction = models.TextField(verbose_name=u'简介')
    teacher = models.ForeignKey(User)
    poster = models.CharField(max_length=100)
    school= models.ForeignKey(School)
    open_date= models.DateField(auto_now=True)
    
    def __unicode__(self):
        return self.title

class Register(models.Model):
    course = models.ForeignKey(Course)
    student = models.ForeignKey(User)

    def __unicode__(self):
        return "{} register {}".format(student,course)
    
    @classmethod
    def is_registered(cls,user,course):
        return cls.objects.filter(course=course,student=user).count() != 0

class Lecture(models.Model):
    title = models.CharField(max_length=100,verbose_name='标题')
    poster = models.CharField(max_length=100,verbose_name='海报')
    teacher = models.ForeignKey(User,verbose_name='老师')
    introduction = models.CharField(max_length=280,null=True,verbose_name='简介')
    course = models.ForeignKey(Course,verbose_name='所属课程')
    open_time= models.DateTimeField(auto_now_add=True,verbose_name='时间')
    duration = models.IntegerField(verbose_name='时长')
    vediourl = models.URLField(verify_exists=False,verbose_name='视频地址')
    outline = models.TextField(verbose_name='大纲')    

    def __unicode__(self):
        return self.title
    
    def vedio_id(self):
        return str(self.vediourl)[29:42]
    
class Reading(models.Model):
    title = models.CharField(max_length=100)
    catalog = models.IntegerField()
    serialno = models.CharField(max_length=20)
    lecture = models.ForeignKey(Lecture)

    def __unicode__(self):
        return self.title

class Assignment(models.Model):
     title = models.CharField(max_length=140)
     description = models.CharField(max_length=500)
     due_date = models.DateField()
     lecture = models.ForeignKey(Lecture)
     
     def __unicode__(self):
         return self.title

def register(user,course):
    if user and user.is_authenticated() and course:
        try:
            register = Register.objects.get(course=course,student=user)
        except :
            register = Register.objects.create(course=course,student=user)
            register.save()
        return register
    return None
    
    