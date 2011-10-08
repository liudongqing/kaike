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
    title = models.CharField(max_length=100)
    introduction = models.TextField()
    teachers = models.ManyToManyField(User)
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
    title = models.CharField(max_length=100)
    poster = models.CharField(max_length=100)
    teacher = models.ForeignKey(User)
    introduction = models.CharField(max_length=280,null=True)
    course = models.ForeignKey(Course)
    open_time= models.DateTimeField()
    duration = models.IntegerField()
    videourl = models.URLField()
    outline = models.TextField()    

    def __unicode__(self):
        return self.title
    
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
    
    