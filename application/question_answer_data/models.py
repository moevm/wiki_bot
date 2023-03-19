from django.db import models

# Create your models here.

class QuestionAnswerData(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    question = models.CharField(max_length=256)
    answer = models.CharField(max_length=256)
    studyYear = models.IntegerField(max_length=1)
    subject = models.CharField(max_length=256)
    date = models.DateTimeField()
    reaction = models.BooleanField()



