from django.db import models
from django import forms
from django.contrib.auth.models import User
import datetime

class InfoPage(models.Model): # used for rules and static pages
    name = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    body_text = models.TextField()
    comments_allowed = models.BooleanField(default=True)
    pub_date = models.DateTimeField(default=datetime.datetime.now())
    mod_date = models.DateTimeField(default=datetime.datetime.now())
    author = models.ForeignKey(User)

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    body_text = models.TextField()
    pub_date = models.DateTimeField(default=datetime.datetime.now())
    author = models.ForeignKey(User)

class NewInfoPageForm(forms.Form):
    name = forms.CharField(max_length=20)
    title = forms.CharField(max_length=100)
    body_text = forms.CharField(widget=forms.Textarea)
    comments_allowed = forms.BooleanField(required=False)

class NewAnnouncementForm(forms.Form):
    title = forms.CharField(max_length=100)
    body_text = forms.CharField(widget=forms.Textarea)
    comments_allowed = forms.BooleanField()
