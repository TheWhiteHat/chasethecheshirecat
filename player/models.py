from django.db import models
from django import forms
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import re

class Team(models.Model):
    name = models.CharField(max_length=50)
    date_joined = models.DateTimeField(default=datetime.datetime.now())
    slogan = models.CharField(max_length=100)
    points = models.IntegerField()
    is_active = models.BooleanField()
    join_key = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/players/team/%i" % self.id

class Player(models.Model):
    user = models.OneToOneField(User)
    team = models.ForeignKey(Team,null=True)
    about = models.TextField()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/players/player/%i" % self.id

class PlayerNameField(forms.CharField):
    def clean(self, value):
        super(PlayerNameField, self).clean(value)
        try:
            User.objects.get(username=value)
            raise forms.ValidationError("Username in use. Please choose another.")
        except User.DoesNotExist:
            return value

class NewPlayerForm(forms.Form):
   name = PlayerNameField(max_length=50)
   password = forms.CharField(widget=forms.PasswordInput,min_length=5)
   password_confirm = forms.CharField(widget=forms.PasswordInput,min_length=5)
   email = forms.EmailField()
   email_confirm = forms.EmailField()
   about = forms.CharField(max_length=300,widget=forms.Textarea)

   def clean_email(self):
   	if self.data['email'] != self.data['email_confirm']:
            raise forms.ValidationError("Emails don't match.")
        return self.data['email']

   def clean_password(self):
        if self.data['password'] != self.data['password_confirm']:
            raise forms.ValidationError("Passwords don't match.")
        if not re.compile('^[a-zA-Z]\w{5,14}$').match(self.data['password']):
            raise forms.ValidationError("Invalid password. Be more secure.")
        return self.data['password']
                                   
   def clean(self,*args, **kwargs):
        self.clean_email()
        self.clean_password()
        return super(NewPlayerForm, self).clean(*args, **kwargs)

class TeamNameField(forms.CharField):
    def clean(self, value):
        super(TeamNameField, self).clean(value)
        try:
            Team.objects.get(name=value)
            raise forms.ValidationError("Team name in use. Please choose another.")
        except Team.DoesNotExist:
            return value

class NewTeamForm(forms.Form):
    name = forms.CharField(max_length=50)
    slogan = forms.CharField(max_length=100)

def create_player_profile(sender,instance, created, **kwargs):
    if created:
        Player.objects.get_or_create(user=instance)

post_save.connect(create_player_profile,sender=User)  
    
