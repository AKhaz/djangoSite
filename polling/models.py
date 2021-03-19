import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    questionText = models.CharField(max_length=250)
    publicationDate = models.DateTimeField('date published')
    points = models.IntegerField(default=0)
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days = 1) <= self.publicationDate <= now
    def __str__(self):
        return self.questionText

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choiceText = models.CharField(max_length=150)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choiceText

class Tag(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    tagText = models.CharField(max_length=20)
    def __str__(self):
        return self.tagText
