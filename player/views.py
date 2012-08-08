from player.models import *
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect


def view_player_info(request,query):
   player = get_object_or_404(Player,id=query)
   return render_to_response("Player_Page.html",{"player":player},context_instance=RequestContext(request))

def view_team_info(request,query):
    team = get_object_or_404(Team,id=query)
    return render_to_response("Team_Page.html",{"team":team},context_instance=RequestContext(request))

def register_new_player(request):
    if request.method == 'POST':
        form = NewPlayerForm(request.POST)
        if form.is_valid():
            try:
                new_user = User(username=form.cleaned_data['name'],password=form.cleaned_data['password'],email=form.cleaned_data['email'])
                new_user.save()
                new_user.get_profile().about = form.cleaned_data['about']
                new_user.save()
            except:
                return HttpResponse(status=500)

            return HttpResponseRedirect('/game/')
    else:
        form = NewPlayerForm()

    return render_to_response("New_Player.html",{'form':form},context_instance=RequestContext(request))
        

#def register_new_team(request):

#def update_team_info(request):

