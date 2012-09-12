from django import template
from player.models import *

register = template.Library()

def top_rankings():
    teams = Team.objects.nonzero_teams().order_by('-points')[0:5]
    return {'teams':teams}

register.inclusion_tag('Top_Rankings_Tag.html')(top_rankings)