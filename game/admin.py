from django.contrib import admin
from game.models import *
from player.models import *
from django import forms

class ChallengeAdmin(admin.ModelAdmin):
    pass
    
class SeriesAdmin(admin.ModelAdmin):
    pass

class SubmissionForm(forms.ModelForm):
    bonus_points = forms.IntegerField(required=False,initial=0)
    class Meta:
        model = Submission

class DeliverableInline(admin.StackedInline):
    model = Deliverable
    can_delete = False
    max_num = 1
    extra = 0

class SubmissionAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_submitted'
    inlines = [DeliverableInline,]
    form = SubmissionForm
    fieldsets = ( 
        (None, {'fields':(('team','date_submitted'))}),
        ('Rate This', {'fields':('is_valid','comment','bonus_points')}),
        )
    readonly_fields = ['challenge','team','date_submitted']
    list_display = ('__unicode__','date_submitted')
    list_filter = ('is_resubmission','deliverable__del_type')

    def queryset(self, request):
            return super(SubmissionAdmin,self).queryset(request).filter(is_valid=None)

    def save_model(self, request, obj, form, change):
        if change:
            if form.cleaned_data['is_valid'] == True:
                points = obj.challenge.points
                bonus_points = 0

                if not form.cleaned_data['bonus_points'] == None:
                    bonus_points = form.cleaned_data['bonus_points']

                team = obj.team
                team.points = team.points + points + bonus_points
                team.save()
        obj.save()

admin.site.register(Challenge)
admin.site.register(Series)
#admin.site.register(Deliverable,DeliverableAdmin)
admin.site.register(Submission,SubmissionAdmin)
