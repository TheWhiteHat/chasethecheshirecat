from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response
from inform.models import *
from django.template import RequestContext
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def view_main_page(request):
    try:
        latest_announcements = Announcement.objects.order_by('-pub_date')[:5]
    except:
        return HttpResponse(status=500)
    return render_to_response("Main_Page.html",{'announcements':latest_announcements},context_instance=RequestContext(request))
    
def view_info_page(request, query):
    page = get_object_or_404(InfoPage,name=query)    
    return render_to_response("Info_Page.html",{'page':page},context_instance=RequestContext(request))
    
def view_announcement(request, query):
    page = get_object_or_404(Announcement,id=query)
    return render_to_response("Announcement.html",{'page':page},context_instance=RequestContext(request))

def list_announcements(request,page_number):
    announcements = get_list_or_404(Announcement)
    paginator = Paginator(announcements,10)

    if page_number == '':
        page_number = 1
    try:
        a_list = paginator.page(page_number)
    except PageNotAnInteger:
        a_list = paginator.page(1)
    except EmptyPage:
         a_list = paginator.page(paginator.num_pages)

    return render_to_response("Announcement_List.html",{'announcements':a_list},context_instance=RequestContext(request))

def create_info_page(request):
    if request.method == 'POST':
        form = NewInfoPageForm(request.POST)
        if form.is_valid():
            try:
                new_info_page = InfoPage(name=form.cleaned_data['name'], title=form.cleaned_data['title'], body_text=form.cleaned_data['body_text'], comments_allowed=form.cleaned_data['comments_allowed'],author=request.user)
                new_info_page.save()
            except:
                return HttpResponse(status=500)
            return HttpResponseRedirect('/')
    else:
        form = NewInfoPageForm()
    
    return render_to_response("New_Info_Page.html",{'form':form},context_instance=RequestContext(request))

def create_announcement(request):
    if request.method == 'POST':
        form = NewAnnouncementForm(request.POST)
        if form.is_valid():
            try:
                new_announcement = Announcement(title=form.cleaned_data['title'],body_text=form.cleaned_data['body_text'], comments_allowed=form.cleaned_data['comments_allowed'],author=request.user)
                new_announcement.save()
            except:
                return HttpResponse(status=500)
            return HttpResponseRedirect('/')
    else:
        form = NewAnnouncementForm()
    
    return render_to_response("New_Announcement.html",{'form':form},context_instance=RequestContext(request))
