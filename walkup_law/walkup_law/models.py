import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models

class Case(models.Model):
    case_number = models.IntegerField()
    attorney = models.CharField(max_length=50)

class Form(models.Model):
    title = models.CharField(max_length=50)
    case = models.AutoField(primary_key=True)

class QuestionGroup(models.Model):
    form = models.ManyToManyField(Form)
    title = models.CharField(max_length=50)
    group_number = models.AutoField()

class Question(models.Model):
    question_group = models.ForeignKey(question_group)