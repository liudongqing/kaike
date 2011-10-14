from django.db import models
from django.forms import ModelForm
from course.models import *



class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields=('title','introduction')

class EditLectureForm(ModelForm):
    class Meta:
        model = Lecture
        fields=('title','introduction','duration','vediourl','outline')

class NewLectureForm(ModelForm):
    class Meta:
        model = Lecture
        exclude =('teacher','course')