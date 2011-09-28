"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from kaike.answers.models import Question,Answer,new_question
from django.contrib import auth
from django.contrib.auth.models import User
from django.test.client import Client;

class AnswersTestCase(TestCase):

    username = "tester"
    password = "test"
    
    def setUp(self):
        User.objects.create_user(AnswersTestCase.username,"test@answers.com",AnswersTestCase.password)
        self.user = auth.authenticate(username = AnswersTestCase.username,password=AnswersTestCase.password)
        

    def test_create_question(self):
        new_question(self.user,title="test",content = "this is a multiline\n questions.",topic="test topic")
        self.assertEqual(Question.objects.get(pk=1).title,'test')
        

