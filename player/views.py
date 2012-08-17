from player.models import * 
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.forms.util import ErrorList
import string
import random


def view_player_info(request,query):
   player = get_object_or_404(Player,id=query)
   return render_to_response("Player_Page.html",{"player":player},context_instance=RequestContext(request))

def view_team_info(request,query):
   team = get_object_or_404(Team,id=query)
   return render_to_response("Team_Page.html",{"team":team},context_instance=RequestContext(request))

def player_home(request):
   if not request.user.is_authenticated() and not request.user.get_profile().is_team_banned:
      return render_to_response("Error.html",{'message':'You are either not logged in or banned.'},context_instance=RequestContext(request))
   player = Player.objects.get(user=request.user)
   if not player.is_confirmed:
      return render_to_response("Player_Home.html",{'is_a_team_member':False},context_instance=RequestContext(request))
   team = player.team;
   unconfirmed_players = team.player_set.exclude(is_confirmed=True)
   return render_to_response("Player_Home.html",{'is_a_team_member':True,'unconfirmed_players':unconfirmed_players},context_instance=RequestContext(request))

def register_new_player(request):
    if request.method == 'POST':
        form = NewPlayerForm(request.POST)
        if form.is_valid():
            try:
                new_user = User()
                new_user.username = form.cleaned_data['name']
                new_user.email = form.cleaned_data['email']
                new_user.set_password(form.cleaned_data['password'])
                new_user.save()
                new_player = Player.objects.get(user=new_user)
                new_player.about = form.cleaned_data['about']
                new_player.save()
                return render_to_response("Success.html",{'message':"You have successfully registered. Please <a href='/login/'>Login</a> to continue."},context_instance=RequestContext(request))
            except:
                return HttpResponse(status=500)

            return HttpResponseRedirect('/game/')
    else:
        form = NewPlayerForm()

    return render_to_response("New_Player.html",{'form':form},context_instance=RequestContext(request))
        
def confirm_player(request,query):
    try:
        player = Player.objects.get(user=request.user)
        unconfirmed_player = Player.objects.get(user=User.objects.get(id=query))
        if not player.team == unconfirmed_player.team:
            return render_to_response("Error.html",{'message':"That player does not want to join your team"},context_instance=RequestContext(request))
        if unconfirmed_player.is_team_banned:
            return render_to_response("Error.html",{'message':"That player is currently banned."},context_instance=RequestContext(request))
        if unconfirmed_player.is_confirmed:
            return render_to_response("Error.html",{'message':"That player is already part of a team."},context_instance=RequestContext(request))
        unconfirmed_player.is_confirmed = True
        unconfirmed_player.save()
    except Player.DoestNotExist:
        return render_to_response("Error.html",{'message':"You are not a player"},context_instance=RequestContext(request))
    except:
        return HttpResponse(status=500)

    return HttpResponseRedirect('/players/home/')

def gen_join_key():
    chars = string.ascii_uppercase + string.digits
    k =  ''.join(random.choice(chars) for x in range(4))
    try:
        Team.objects.get(join_key=k)
        return gen_join_key()
    except Team.DoesNotExist: 
        return k

def register_new_team(request):
    if request.method == 'POST':
        form = NewTeamForm(request.POST)
        if form.is_valid():
            try: 
               new_team = Team(name=form.cleaned_data['name'],slogan=form.cleaned_data['slogan'],join_key=gen_join_key())
               new_team.save()
               player = Player.objects.get(user=request.user)
               player.team = new_team
               player.is_confirmed = True
               player.save()
               return render_to_response("Success.html",{'message':"You have successfully registerd a new team. <a href='/players/home/'>Continue</a>"},context_instance=RequestContext(request))
            except:
               return HttpReponse(status=500)
    else:
        form = NewTeamForm()

    return render_to_response("New_Team.html",{'form':form},context_instance=RequestContext(request))


def join_team(request):
    if request.method == 'POST':
        form = JoinTeamForm(request.POST)
        if form.is_valid():
            try:
               team = get_object_or_404(Team,join_key=form.cleaned_data['join_key'],is_active=True)
               if team.count_players() >= 5:
                   return render_to_response("Error.html",{'message':'That team already has more than 5 members.'},context_instance=RequestContext(request))
               player = Player.objects.get(user=request.user)
               player.team = team;
               player.is_confirmed = False
               player.is_team_banned = False
               player.save()
               return render_to_response("Success.html",{'message':"You have submitted a request to join the team. Please wait until another user confirms you. <a href='/players/home/'>Continue</a>"},context_instance=RequestContext(request))
            except:
                return HttpResponse(status=500)
    else:
            form = JoinTeamForm()

    return render_to_response("Join_Team.html",{'form':form},context_instance=RequestContext(request))

def leave_team(request):
    if request.method == 'GET' and 'confirm' in request.GET and request.GET['confirm'] == 'true': 
        try:    
            player = Player.objects.get(user=request.user)
            player.team = None
            player.is_confirmed = False
            player.is_team_banned = False
            player.save()
            return render_to_response("Success.html",{'message':"You have successfully left the team. <a href='/game/'>Continue</a>"},context_instance=RequestContext(request))
        except:
            return HttpResponse(status=500)
    else:
        return render_to_response("Leave_Team.html",context_instance=RequestContext(request))

def request_ban(request):
    if request.method == 'POST':
        form = RequestBanForm(request.POST)
        if form.is_valid():
            try:
                bad_player = Player.objects.get(user=User.objects.get(username=form.cleaned_data['username']))
                requested_by = Player.objects.get(user=request.user)
                if bad_player == requested_by:
                    errors = form._errors.setdefault("username", ErrorList())
                    errors.append(u"You may not ban yourself.")
                    return render_to_response("Request_Ban.html",{'form':form},context_instance=RequestContext(request))
                ban_request = BanRequest(requested_by=requested_by,bad_player=bad_player,reason=form.cleaned_data['reason']) 
                ban_request.save() 
                return render_to_response("Success.html",{'message':"You have successfully submitted a ban request. <a href='/game/'>Continue</a>"},context_instance=RequestContext(request))
            except:
                return HttpResponse(status=500)
    else:
        form = RequestBanForm()

    return render_to_response("Request_Ban.html",{'form':form},context_instance=RequestContext(request))

def update_team_info(request):
    if request.method == 'POST':
        form = UpdateTeamInfoForm(request.POST)
        if form.is_valid():
            try:
                player = Player.objects.get(user=request.user)
                team = player.team
                team.slogan = form.cleaned_data['slogan']
                team.save()
                return render_to_response("Success.html",{'message':"Team info successfully updated. <a href='/players/home/'>Continue</a>'"},context_instance=RequestContext(request))
            except:
                return HttpResponse(status=500)
    else:
        form = UpdateTeamInfoForm()

    return render_to_response("Update_Team_Info.html",{'form':form},context_instance = RequestContext(request))

def update_player_info(request):
    if request.method == 'POST':
        form = UpdatePlayerInfoForm(request.POST)
        if form.is_valid():
            try:
                player = Player.objects.get(user=request.user)
                player.about = form.cleaned_data['about']
                player.save()
                return render_to_response("Success.html",{'message':"Player info successfully updated. <a href='/players/home/'>Continue</a>'"},context_instance=RequestContext(request))
            except:
                return HttpResponse(status=500)
    else:
        form = UpdatePlayerInfoForm()

    return render_to_response("Update_Player_Info.html",{'form':form},context_instance = RequestContext(request))
