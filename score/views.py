from django.shortcuts import render_to_response
from player.models import *
from django.template import RequestContext
from django.core.context_processors import csrf

def score(request):
    teams = Team.objects.nonzero_teams().order_by('-points')
    return render_to_response("Score.html",{'teams':teams},context_instance=RequestContext(request))
