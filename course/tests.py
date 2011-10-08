from django.test import TestCase
from kaike.course.models import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.test.client import Client
import datetime

class RegisterTestCase(TestCase):

    username = "tester"
    password = "test"    
        
    def setUp(self):
        school = School.objects.create(name='aschool',address='my school address',website='http://test')
        school.save();
        course = Course.objects.create(title='test',introduction='test introduction',poster='fakeposter',school=school)
        print course
        course.save()
        
        User.objects.create_user(RegisterTestCase.username,"test@answers.com",RegisterTestCase.password)
        self.user = auth.authenticate(username = RegisterTestCase.username,password=RegisterTestCase.password)
        print Course.objects.all()
        self.course = Course.objects.get(title='test')

    def test_register(self):
        register(self.user,self.course)
        self.assertEqual(Register.objects.all().count(),1)
        register(self.user,self.course)
        self.assertEqual(Register.objects.all().count(),1)

