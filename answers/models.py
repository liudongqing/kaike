from django.db import models
from django.contrib.auth.models import User
import time
# Create your models here.

class Question(models.Model):
    title = models.CharField(max_length=255)
    timestamp = models.CharField(max_length=50)
    user= models.ForeignKey(User)
    content = models.TextField( max_length=3000)
    topic  = models.TextField()
    
    def __unicode__(self):
        return self.title
    
def new_question(user,title, content,topic):
    """
    create new question only if the given user is logged in. or else raise Error
    """
    if user and user.is_authenticated():
        return Question.objects.create(user = user,title=title,content=content,timestamp=time.time(),topic =topic)
    else:
        raise Exception("User not authenticated")
        
class Answer(models.Model):
    timestamp = models.CharField(max_length=50)
    user= models.ForeignKey(User)
    content = models.TextField( max_length=3000)
    question = models.ForeignKey(Question)
    
    def __unicode__(self):
        return self.title

def new_answer(user,question,content):
    if user and user.is_authenticated():
        return Answer.objects.create(user = user,question=question,content=content,timestamp=time.time())
    else:
        raise Exception("User not authenticated")
