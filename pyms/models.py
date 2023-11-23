from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=100)
    School = models.CharField(max_length=100)
    Grade = models.IntegerField(default=0)
    Class = models.IntegerField(default=0)
    Number = models.IntegerField(default=0)
    is_teacher = models.BooleanField(default=False)


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    School = models.CharField(max_length=100)
    Grade = models.IntegerField(default=0)
    nickname = models.CharField(max_length=100)
    is_teacher = models.BooleanField(default=False)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    private = models.CharField(max_length=100, default="", null=True)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')
    imgfile = models.ImageField(null=True, upload_to="", blank=True)

    def __str__(self):
        return f"{self.id}, {self.subject}, {self.content}"


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='author_answer')
    School = models.CharField(max_length=100)
    Grade = models.IntegerField(default=0)
    nickname = models.CharField(max_length=100)
    is_teacher = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')
    imgfile = models.ImageField(null=True, upload_to="", blank=True)


class RegisteredSchool(models.Model):
    school = models.CharField(max_length=100, unique=True)
