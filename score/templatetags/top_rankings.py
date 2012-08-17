from django import template
from player.models import *

register = template.Library()

def top_rankings():
    teams = Team.objects.order_by('-points').all()[0:5]
    return {'teams':teams}

register.inclusion_tag('Top_Rankings_Tag.html')(top_rankings)