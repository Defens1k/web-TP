# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from datetime import datetime
from django.contrib.auth.models import User, AbstractUser
from django.dispatch import receiver
from django.urls import reverse
from django.db.models.signals import post_save
from django.utils import timezone
from django.db import models

class QuestionManager(models.Manager):
    def all_new(self):
        return self.order_by('-publication_date').all()

    def all_rate(self):
        return self.order_by('-raiting').all()

    def all_questions_by_tag(self, tag_name):
        return self.filter(tag__name = tag_name).all()


class AnswerManager(models.Manager):
    def all_answers_by_question(self, question_id):
        return self.filter(question__pk = question_id).all()


class TagManager(models.Manager):
    def get_popular_tags(self):
        return self.all()[:5]


class Tag(models.Model):
    name = models.CharField(max_length=255,verbose_name=u'Имя')
    objects = TagManager()


class Profile(models.Model):
    avatar = models.ImageField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    raiting = models.IntegerField(null=True, blank=True, default=0)


class Question(models.Model):
    title = models.CharField(max_length=255,verbose_name=u'Заголовок')
    text = models.TextField(verbose_name=u'Текст')
    tag = models.ManyToManyField(Tag)
    author = models.ForeignKey(Profile, on_delete=models.PROTECT, verbose_name=u'Автор')
    raiting = models.IntegerField(null=True, blank=True, default=0)
    publication_date = models.DateTimeField(default=timezone.now(), blank=True, verbose_name=u'Дата публикации')
    manager = QuestionManager()


class Answer(models.Model):
    text = models.TextField(verbose_name=u'Текст')
    question = models.ForeignKey(Question, on_delete=models.PROTECT, verbose_name=u'Вопрос')
    author = models.ForeignKey(Profile, on_delete=models.PROTECT, verbose_name=u'Автор', null=True)
    raiting = models.IntegerField(null=True, blank=True, default=0)
    manager = AnswerManager()


class Like(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.PROTECT, verbose_name=u'Автор', null=True)
    answer = models.ForeignKey(Answer, on_delete=models.PROTECT, verbose_name=u'Ответ', null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.PROTECT, verbose_name=u'Вопрос', null=True, blank=True)

