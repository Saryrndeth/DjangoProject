from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=100, default="", null=True)
    School = models.CharField(max_length=100)
    Grade = models.IntegerField(default=0)
    Class = models.IntegerField(default=0)
    Number = models.IntegerField(default=0)
    is_teacher = models.BooleanField(default=False)


class Question(models.Model):
    School = models.CharField(max_length=100, default="", null=True)
    Grade = models.IntegerField(default=0)
    is_teacher = models.BooleanField(default=False)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return f"{self.id}, {self.subject}, {self.content}"


class Answer(models.Model):
    School = models.CharField(max_length=100, default="", null=True)
    Grade = models.IntegerField(default=0)
    is_teacher = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()


class RegisteredSchool(models.Model):
    school = models.CharField(max_length=100, unique=True)
