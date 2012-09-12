from django.db import models
from django import forms
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import re
from game.models import *

class NonZeroTeams(models.Manager):
    def nonzero_teams(self):
        teams = self.filter(is_active=True)
        for t in teams:
            if t.count_players() <= 0:
                teams = teams.exclude(id=t.id)
        return teams

class Team(models.Model):
    name = models.CharField(max_length=50)
    date_joined = models.DateTimeField(default=datetime.datetime.now())
    slogan = models.CharField(max_length=100)
    points = models.IntegerField(default=0)
    series_unlocked = models.ManyToManyField('game.Series',blank=True)
    is_active = models.BooleanField(default=True)
    join_key = models.CharField(max_length=10)
    objects = NonZeroTeams()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/players/team/%i" % self.id

    def count_players(self):
        n = 0
        for p in self.player_set.all():
            if p.is_confirmed and not p.is_team_banned:
                n+=1
        return n
    
    
class Player(models.Model):
    user = models.OneToOneField(User)
    team = models.ForeignKey(Team,null=True)
    about = models.TextField()
    is_confirmed = models.BooleanField(default=False)
    is_team_banned = models.BooleanField(default=False)
    is_judge = models.BooleanField(default=False)


    def __unicode__(self):
        return self.user.username

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
        if not re.compile('^[a-zA-Z]\w{5,25}$').match(self.data['password']):
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
    name = TeamNameField(max_length=50)
    slogan = forms.CharField(max_length=100)

class TeamKeyField(forms.CharField):
    def clean(self,value):
        super(TeamKeyField,self).clean(value)
        try:
            team = Team.objects.get(join_key=value,is_active=True)
            if team.count_players() >= 5:
                raise forms.ValidationError("Team cannot accept more players.")
            return value
        except Team.DoesNotExist:
            raise forms.ValidationError("That team does not exist.")

class JoinTeamForm(forms.Form):
    join_key = TeamKeyField(max_length=10)

class PlayerNameBanField(forms.CharField):
    def clean(self, value):
        super(PlayerNameBanField, self).clean(value)
        try:
            if Player.objects.get(user=User.objects.get(username=value)).is_judge:
                raise forms.ValidationError("You may not ban a judge.")
            return value
        except User.DoesNotExist:
            raise forms.ValidationError("This user does not exist.")

class RequestBanForm(forms.Form):
    username = PlayerNameBanField(max_length=50)
    reason = forms.CharField(max_length=300,widget=forms.Textarea)

    def clean(self,*args, **kwargs):
        return super(RequestBanForm, self).clean(*args,**kwargs)

class BanRequest(models.Model):
   requested_by = models.ForeignKey(Player, related_name='banrequest_requested_by')
   bad_player = models.ForeignKey(Player, related_name='banrequest_bad_player')
   reason = models.TextField()
   date_submitted = models.DateTimeField(default=datetime.datetime.now())

class UpdateTeamInfoForm(forms.Form):
    slogan = forms.CharField(max_length=100)

class UpdatePlayerInfoForm(forms.Form):
    about = forms.CharField(max_length=400,widget=forms.Textarea)

def create_player_profile(sender,instance, created, **kwargs):
    if created:
        Player.objects.get_or_create(user=instance)

post_save.connect(create_player_profile,sender=User)  
    
