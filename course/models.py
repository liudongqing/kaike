from django.db import models

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    website = models.URLField()

    def __unicode__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField()

    def __unicode__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=100)
    teachers = models.ManyToManyField(Teacher)
    school= models.ForeignKey(School)
    open_date= models.DateField()
    

    def __unicode__(self):
        return self.title

class Reading(models.Model):
    title = models.CharField(max_length=100)
    catalog = models.IntegerField()
    serialno = models.CharField(max_length=20)

    def __unicode__(self):
        return self.title

class Assignment(models.Model):
     title = models.CharField(max_length=140)
     description = models.CharField(max_length=500)
     due_date = models.DateField()

     def __unicode__(self):
         return title

class Lecture(models.Model):
    title = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher)
    open_time= models.DateTimeField()
    duration = models.IntegerField()
    assignments = models.ManyToManyField(Assignment)
    readings =  models.ManyToManyField(Reading)

    def __unicode__(self):
        return title
