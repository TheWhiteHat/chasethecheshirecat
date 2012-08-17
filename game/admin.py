from django.contrib import admin
from game.models import *
from player.models import *

class ChallengeAdmin(admin.ModelAdmin):
    pass
    
class SeriesAdmin(admin.ModelAdmin):
    pass

class DeliverableAdmin(admin.ModelAdmin):
    pass

class SubmissionAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change):
        if change:
            if form.cleaned_data['is_valid'] == True:
                points = obj.challenge.points
                team = obj.team
                team.points = team.points + points
                team.save()
        obj.save()

admin.site.register(Challenge)
admin.site.register(Series)
admin.site.register(Deliverable)
admin.site.register(Submission,SubmissionAdmin)