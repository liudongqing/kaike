from django.db import models

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    website = models.URLField()

    def __unicode__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField()
    douban_id = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=100)
    introduction = models.TextField()
    teachers = models.ManyToManyField(User)
    poster = models.CharField(max_length=100)
    school= models.ForeignKey(School)
    open_date= models.DateField()
    
    def __unicode__(self):
        return self.title

class Register(models.Model):
    course = models.ForeignKey(Course)
    student = models.ForeignKey(User)
    reg_type = models.IntegerField()

    def __unicode__(self):
        return "{} register {}".format(student,course)


class Lecture(models.Model):
    title = models.CharField(max_length=100)
    poster = models.CharField(max_length=100)
    teacher = models.ForeignKey(User)
    introduction = models.CharField(max_length=280,null=True)
    course = models.ForeignKey(Course)
    open_time= models.DateTimeField()
    duration = models.IntegerField()

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

