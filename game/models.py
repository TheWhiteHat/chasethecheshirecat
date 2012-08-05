from django.db import models

DEL_CHOICES = (('image','Image'),('video','Video'),('audio','Audio'),('physical','Physical'),('key','Key'),)

class Challenge(models.Model):
    CAT_CHOICES = (('silly', 'Silly'),('hacking','Hacking'),('promote','Promote'),('crypto','Crypto'),)
    name = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField(default=datetime.datetime.now())
    due_date = models.DateTimeField()
    category = models.CharField(max_length=15,choices=CAT_CHOICES)
    deliverable = models.CharField(max_length=15,choices=DEL_CHOICES)
    points = models.IntegerField()

class Deliverable(models.Model):
    DEL_CHOICES = (('image','Image'),('video','Video'),('audio','Audio'),('physical','Physical'),('key','Key'),)
    del_type = models.CharField(max_length=15,choices=DEL_CHOICES)
    uploaded_file = models.FileField(upload_to="submissions/",blank=True)

class Submission(models.Model):
    challenge = models.ForeignKey(Challenge)
    team = models.ForeignKey(Team)
    date_submitted = models.DateTimeField(default=datetime.datetime.now())
    is_valid = models.BooleanField(blank=True)
    deliverable =  models.ForeignKey(Deliverable)        
