from django.db import models
from player.models import *
import datetime

DEL_CHOICES = (('image','Image'),('video','Video'),('audio','Audio'),('physical','Physical'),('key','Key'),)

class Series(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    qrcode = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name

class Challenge(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    series = models.ForeignKey(Series)
    pub_date = models.DateTimeField(default=datetime.datetime.now())
    due_date = models.DateTimeField(null=True)
    deliverable = models.CharField(max_length=15,choices=DEL_CHOICES)
    points = models.IntegerField()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/game/challenge/%i" % self.id

class Deliverable(models.Model):
    del_type = models.CharField(max_length=15,choices=DEL_CHOICES)
    key = models.CharField(max_length=300,blank=True)
    uploaded_file = models.FileField(upload_to="submissions/",blank=True)

    def __unicode__(self):
        return str(self.id)

class Submission(models.Model):
    challenge = models.ForeignKey(Challenge)
    team = models.ForeignKey('player.Team')
    date_submitted = models.DateTimeField(default=datetime.datetime.now())
    is_valid = models.NullBooleanField(null=True,default=None)
    is_resubmission = models.BooleanField(default=False)
    comment = models.TextField(blank=True)
    deliverable =  models.ForeignKey(Deliverable)
    
    def __unicode__(self):
        return self.team.name + " " + self.challenge.name

    def get_absolute_url(self):
        return "/game/submission/%i" % self.id

class ChallengeIdField(forms.CharField):
    def clean(self,value):
        super(ChallengeIdField, self).clean(value)
        try:
            Challenge.objects.get(id=value)
            return value
        except Challenge.DoesNotExist:
            raise forms.ValidationError("Not a valid challenge.")
        
class SubmitKeyForm(forms.Form):
    key = forms.CharField(widget=forms.Textarea,max_length=300)
    challenge_id = ChallengeIdField(widget=forms.HiddenInput)

class SubmitFileForm(forms.Form): #this form will be used only when a user doesn't have javascript on. 
   thefile = forms.FileField()
   challenge_id = ChallengeIdField()

class UnlockCodeField(forms.CharField):
    def clean(self,value):
        super(UnlockCodeField, self).clean(value)
        try:
            Series.objects.get(qrcode=value)
            return value
        except Series.DoesNotExist:
            raise forms.ValidationError("Not a valid code.")

class UnlockSeriesForm(forms.Form):
    code = UnlockCodeField(max_length=10)
    
    def clean(self, *args, **kwargs):
        return super(UnlockSeriesForm, self).clean(*args, **kwargs)
