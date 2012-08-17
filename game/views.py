from game.models import *
from player.models import *
from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response
from django.core.context_processors import csrf
from django.middleware.csrf import get_token
from django.utils import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

def game_home(request):
    "Returns a homepage for the game, with game-related actions, latest challenges, and top rankings."
    if request.user.is_authenticated:
        if request.user.get_profile().is_confirmed:
            try:
                team = Player.objects.get(is_confirmed=True,user=request.user).team
                challenges = []

                for s in team.series_unlocked.all():
                    for c in Challenge.objects.filter(series=s).all():
                        challenges.append(c)

                return render_to_response("Game_Home.html",{'challenges':challenges[0:4]},context_instance=RequestContext(request))
            
            except Player.DoesNotExist:
                return render_to_response("Error.html",{'message':"You are not a user."},context_instance=RequestContext(request))
            #except:
             #   return HttpResponse(status=500)
        else:   
            return render_to_response("Error.html",{'message':"You are not on a team."},context_instance=RequestContext(request))
            
    else:
        return render_to_response("Error.html",{'message':"You are not logged in."},context_instance=RequestContext(request))

def list_challenges(request,page_number):
    "Returns a paginated list of challenges based on unlocked series and submissions."
    if request.user and request.user.is_authenticated and request.user.get_profile().is_confirmed and not request.user.get_profile().is_team_banned:
        team = Player.objects.get(is_confirmed=True,user=request.user).team
        challenges = []
            
        for s in team.series_unlocked.all():
            for c in Challenge.objects.filter(series=s).all():
                challenges.append(c)           
    
        paginator = Paginator(challenges,10)

        if page_number == '':
            page_number = 1
        try:
            c_list = paginator.page(page_number)
        except PageNotAnInteger:
            c_list = paginator.page(1)
        except EmptyPage:
            c_list = paginator.page(paginator.num_pages)
        return render_to_response("Challenge_List.html",{'challenges':c_list},context_instance=RequestContext(request))   
    else:
        return render_to_response("Error.html",{'message':"You are either not logged in or not on a team"},context_instance=RequestContext(request))

    
def view_challenge(request,query):
    "Returns an info page for a given challenge id (query)"
    challenge = get_object_or_404(Challenge,id=query)
    if request.user and request.user.is_authenticated and request.user.get_profile().is_confirmed and not request.user.get_profile().is_team_banned:
        team = Player.objects.get(is_confirmed=True,user=request.user).team
        if team.series_unlocked.filter(id=challenge.series.id).exists():
            try:
                if Submission.objects.filter(team=team,challenge=challenge,is_valid=True).exists():
                    return render_to_response("View_Challenge.html",{'challenge':challenge,'submit_allowed':False,'completed':True},context_instance=RequestContext(request))
                submission = Submission.objects.get(team=team,challenge=challenge,is_valid=None)
                return render_to_response("View_Challenge.html",{'challenge':challenge,'submit_allowed':False,'completed':False},context_instance=RequestContext(request))
            except Submission.DoesNotExist:
                request.session['current_challenge'] = query
                return render_to_response("View_Challenge.html",{'challenge':challenge,'submit_allowed':True,'completed':False},context_instance=RequestContext(request))
        else:
            return render_to_response("Error.html",{'message':"You have not unlocked this challenge yet."},context_instance=RequestContext(request))
    else:
        return render_to_response("Error.html",{'message':"You are either not logged in or not on a team"},context_instance=RequestContext(request))
    
def list_submissions(request,page_number):
    "Returns a paginated list of a team's submissions"
    if request.user and request.user.is_authenticated and request.user.get_profile().is_confirmed and not request.user.get_profile().is_team_banned:
        try:
            player = Player.objects.get(user=request.user)
            if player.team and player.is_confirmed:
                submissions = player.team.submission_set.all()
                return render_to_response("Submission_List.html",{'submissions':submissions},context_instance=RequestContext(request))
            else:
                return render_to_response("Error.html",{'message':"You are not currently part of any team."},context_instance=RequestContext(request))
        except Player.DoesNotExist:
            return render_to_response("Error.html",{'message':"You are not a user."},context_instance=RequestContext(request))
    else:
        return render_to_response("Error.html",{'message':"You are either not logged in or not on a team"},context_instance=RequestContext(request))

def view_submission(request,query):
    "Returns an info page of a single submission"
    if request.user and request.user.is_authenticated and request.user.get_profile().is_confirmed and not request.user.get_profile().is_team_banned:
        try:
            player = Player.objects.get(user=request.user)
            if player.team and player.is_confirmed:
                submission = get_object_or_404(Submission,id=query)
                return render_to_response("View_Submission.html",{'submission':submission},context_instance=RequestContext(request))
            else:
                return render_to_response("Error.html",{'message':"You are not currently part of any team."},context_instance=RequestContext(request))
        except Player.DoesNotExist:
                return render_to_response("Error.html",{'message':"You are not a user."},context_instance=RequestContext(request))
        except:
            return HttpResponse(status=500)
    else:
        return render_to_response("Error.html",{'message':"You are either not logged in or not on a team"},context_instance=RequestContext(request))
    

def save_upload( uploaded, filename, raw_data, team, challenge, is_resub ):
    "Writes an upload to the disk."
    import os.path
    if is_resub:
        sub = "resub"
    else:
        sub =''
    filename = settings.MEDIA_ROOT + str(challenge.id) + "_" + team.name.replace (" ", "_") + sub + "." + os.path.splitext(filename)[1][1:].strip()
    try:
      from io import FileIO, BufferedWriter
      with BufferedWriter( FileIO( filename, "wb" ) ) as dest:
        if raw_data:
          foo = uploaded.read( 1024 )
          while foo:
            dest.write( foo )
            foo = uploaded.read( 1024 ) 
        else:
          for c in uploaded.chunks( ):
            dest.write( c )
        deliverable = Deliverable(del_type=challenge.deliverable,uploaded_file=filename)
        deliverable.save()
        submission = Submission(challenge=challenge,team=team,is_resubmission=is_resub,deliverable=deliverable)
        submission.save()
        return True
    except IOError:
      pass
    return False
    
def submit_file(request,query):
    "Returns an file submission page and handles an upload/submission."
    if request.user and request.user.is_authenticated and request.user.get_profile().is_confirmed and not request.user.get_profile().is_team_banned:
        if request.method == 'POST':
            if request.is_ajax(): 
                if not request.GET['challenge_id'] == request.session['current_challenge']:
                    json_response = {'success':False,'error':'Invalid challenge id.'}
                    return HttpResponse(json.dumps(json_response))
                upload = request
                is_raw = True
                challenge_id = request.GET['challenge_id']
                try:
                    filename = request.GET['qqfile']
                except KeyError:
                    return HttpResponseBadRequest('Lame ajax request')
            else:
                is_raw = False
                form = SubmitFileForm(request.POST,request.FILES)
                if form.is_valid():
                    upload = request.FILES['thefile']
                    filename = upload.name
                    challenge_id = form.changed_data['challenge_id']
                  
            challenge = Challenge.objects.get(id=challenge_id)
            is_resub = Submission.objects.filter(team=request.user.get_profile().team,challenge=challenge,is_valid=False).exists()
            team = Player.objects.get(is_confirmed=True,user=request.user).team
            
            if Submission.objects.filter(team=team,challenge=challenge,is_valid=None).exclude(is_valid=False).exists():
                success = False
            else:
                success = save_upload(upload, filename, is_raw, request.user.get_profile().team, challenge, is_resub)

            json_response = {'success':success,}
            return HttpResponse(json.dumps(json_response))
        else:
            try:
                challenge = get_object_or_404(Challenge,id=query)
                team = Player.objects.get(is_confirmed=True,user=request.user).team
                submission = Submission.objects.get(team=team,challenge=challenge,is_valid=None)
                return render_to_response("Error.html",{'message':"This submission is pending judge approval, resubmissions are not allowed yet."},context_instance=RequestContext(request))
            except Submission.DoesNotExist:
                csrf_token = get_token(request)
                return render_to_response("Submit_File.html",{'csrf_token':csrf_token,'del_type':challenge.deliverable,'challenge_id':challenge.id},context_instance=RequestContext(request))
    else:
        return render_to_response("Error.html",{'message':"You are either not logged in or not on a team"},context_instance=RequestContext(request))

def submit_key(request,query):
    "Returns a key submission page and handles a submission"
    if request.user and request.user.is_authenticated and request.user.get_profile().is_confirmed and not request.user.get_profile().is_team_banned:
        if request.method == 'POST':
            form = SubmitKeyForm(request.POST)
            if form.is_valid():
                try:
                    if not form.cleaned_data['challenge_id'] == request.session['current_challenge']:
                        return render_to_response("Error.html",{'message':'Wrong submission id.'},context_instace=RequestContext(request))
                    challenge = Challenge.objects.get(id=form.cleaned_data['challenge_id'])
                    team = Player.objects.get(is_confirmed=True,user=request.user).team
                    deliverable = Deliverable(del_type='key',key=form.cleaned_data['key'])
                    deliverable.save()
                    submission = Submission(challenge=challenge,team=team,deliverable=deliverable)
                    submission.save()
                    return render_to_response("Success.html",{'message':'Successfully made submission.'},context_instance=RequestContext(request))
                except Challenge.DoesNotExist:
                    errors = form._errors.setdefault("challenge_id", ErrorList())
                    errors.append(u"Invalid Challenge ID")
                    return render_to_response("Submit_Key.html",{'form':form},context_instance=RequestContext(request))
                except Team.DoesNotExist:                 
                    return render_to_response("Error.html",{'message':"You are not on a team."},context_instance=RequestContext(request))
        else:
            form = SubmitKeyForm()
        
        return render_to_response("Submit_Key.html",{'form':form},context_instance=RequestContext(request))
    else:
        return render_to_response("Error.html",{'message':"You are either not logged in or not on a team"},context_instance=RequestContext(request))

def unlock_series(request):
    "Unlocks a series of challenges for a team given a qrcode."
    if request.user and request.user.is_authenticated and request.user.get_profile().is_confirmed and not request.user.get_profile().is_team_banned:
        if request.method == 'POST':
            form = UnlockSeriesForm(request.POST)
            if form.is_valid():
                try:
                    team = Player.objects.get(is_confirmed = True,user=request.user).team
                    series = Series.objects.get(qrcode = form.cleaned_data['code'])
                    if team.series_unlocked.filter(qrcode=series.qrcode).exists():
                        return render_to_response("Error.html",{'message':"You have already added that series."},context_instance=RequestContext(request))
                    else:
                        team.series_unlocked.add(series)
                        team.save()
                        return render_to_response("Success.html",{'message':"Successfully added the series."},context_instance=RequestContext(request))
                except Team.DoesNotExist:
                    return render_to_response("Error.html",{'message':"You are not on a team."},context_instance=RequestContext(request))
                except Player.DoesNotExist:
                    return render_to_response("Error.html",{'message':"You are not a user."},context_instance=RequestContext(request))
                except Series.DoesNotExist:
                    return render_to_response("Error.html",{'message':"This error should not happen. Anyways, invalid code specified."},context_instance=RequestContext(request))
                except:
                    return HttpResponse(status=500)
    
        else:
            form = UnlockSeriesForm()
    
        return render_to_response("Unlock_Series.html",{'form':form},context_instance=RequestContext(request))
    else:
        return render_to_response("Error.html",{'message':"You are either not logged in or not on a team"},context_instance=RequestContext(request))
