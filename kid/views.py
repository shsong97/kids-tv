# -*- coding:utf-8 -*-

from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.utils.http import is_safe_url
from django.utils.translation import gettext as _

from django.template import Context, RequestContext
from django.template.loader import get_template

from django.contrib.auth import logout, login 
from django.contrib.auth.models import User
from django.contrib.auth.forms import * 
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import password_reset, password_reset_confirm

from django.shortcuts import render,render_to_response, redirect,get_object_or_404

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse

from django.db.models import Q

from datetime import datetime, timedelta
from kid.models import *
from kid.forms import *


login_url='/login'
ITEMS_PER_PAGE=10
PAGE_COUNT = 10

def home(request, cat_name1='All', cat_name2=''):
    name=cat_name1+'/'+cat_name2
    search_field = ''
    category1 = Category1.objects.order_by('title')
    if cat_name2 != '':
        cat2=get_object_or_404(Category2,title=cat_name2)
        kids_items=cat2.kid_set.order_by('-update_date')
    else:
        kids_items = Kid.objects.order_by('-update_date')

    paginator=Paginator(kids_items,ITEMS_PER_PAGE)

    try:
        page=int(request.GET['page'])
    except:
        page=1
    try:
        kids_items=paginator.page(page)
    except:
        raise Http404

    page_list = []
    
    has_prev10=False
    has_next10=False
    prev_page10=0
    next_page10=0

    total_page = paginator.num_pages
    if total_page > PAGE_COUNT and page + PAGE_COUNT < total_page:
        has_next10 = True
        next_page10 = (( page + PAGE_COUNT ) / PAGE_COUNT) * PAGE_COUNT
    
    if page > PAGE_COUNT:
        has_prev10 = True
        prev_page10 = (( page - PAGE_COUNT ) / PAGE_COUNT) * PAGE_COUNT

    from_page = ( page / PAGE_COUNT ) * PAGE_COUNT + 1
    
    if from_page + PAGE_COUNT < total_page:
        page_size = PAGE_COUNT
    else:
        page_size = total_page
    
    for i in range(page_size):
        page_list.append((i+from_page))

    context = RequestContext(request,
                             {  'category1': category1,
                                'kids_items': kids_items,
                                'name' : name,
                                'search_field' : search_field,
                                'show_paginator':paginator.num_pages>1,
                                'has_prev':kids_items.has_previous(),
                                'has_next':kids_items.has_next(),
                                'page':page,
                                'pages':paginator.num_pages,
                                'page_list' : page_list,
                                'next_page':page+1, 
                                'prev_page':page-1,
                                'has_prev10':has_prev10,
                                'has_next10':has_next10,
                                'prev_page10':prev_page10,
                                'next_page10':next_page10,                                
                              })
    return render_to_response('search.html', context)


def schedule(request):
    search_field = ''
    if request.GET.has_key('search_field'):
        if request.GET['search_field'] is not None:
            search_field=request.GET['search_field']
            
    page = '1'
    if request.GET.has_key('page'):
        if request.GET['page'] is not None:
            page=request.GET['page']

    page_url = '&page=' + page

    category1 = Category1.objects.order_by('title')
    category2 = Category2.objects.order_by('title')
                              
    from bs4 import BeautifulSoup
    import urllib

    kids_items = []
    if search_field != '':
        youtube_url ='https://www.youtube.com'
        url = youtube_url + '/results?search_query=' + search_field.encode('utf-8') + page_url.encode('utf-8')
        html_doc = urllib.urlopen(url)
        soup = BeautifulSoup(html_doc)
        links = soup.findAll('div', attrs={'class':'yt-lockup-dismissable'})
        
        for link in links:
            title = link.find('h3').find('a')['title']
            h_url = youtube_url + link.find('h3').find('a')['href']
            i_url = link.find('div',attrs={'class':'video-thumb'}).find('img')
            image_url=''
            try:
                if i_url['data-thumb'] != '':
                    image_url=i_url['data-thumb']
                else:
                    image_url=i_url['src']
            except:
                image_url=i_url['src']
                
            kids_items.append( (title,h_url,image_url ))

    context = RequestContext(request,
                             {'category1' : category1,
                              'category2' : category2,
                              'kids_items' : kids_items,
                              'search_field' : search_field,
                              'page' : page,
                              })
    return render_to_response('schedule.html', context)

def search(request):
    category1 = Category1.objects.order_by('title')
    search_field = ''
    if request.GET.has_key('search_field'):
        if request.GET['search_field'] is not None:
            search_field = request.GET['search_field']
            kids_items = Kid.objects.filter(title__icontains=search_field).order_by('-update_date')
    else:
        kids_items = Kid.objects.order_by('-update_date')
    
    paginator=Paginator(kids_items,ITEMS_PER_PAGE)

    try:
        page=int(request.GET['page'])
    except:
        page=1
    try:
        kids_items=paginator.page(page)
    except:
        raise Http404

    has_prev10=False
    has_next10=False
    prev_page10=0
    next_page10=0

    total_page = paginator.num_pages
    if total_page > PAGE_COUNT and page + PAGE_COUNT < total_page:
        has_next10 = True
        next_page10 = (( page + PAGE_COUNT ) / PAGE_COUNT) * PAGE_COUNT
    
    if page > PAGE_COUNT:
        has_prev10 = True
        prev_page10 = (( page - PAGE_COUNT ) / PAGE_COUNT) * PAGE_COUNT

    from_page = ( page / PAGE_COUNT ) * PAGE_COUNT + 1
    
    if from_page + PAGE_COUNT < total_page:
        page_size = PAGE_COUNT
    else:
        page_size = total_page
    
    for i in range(page_size):
        page_list.append((i+from_page))
        
    context = RequestContext(request,
                             {'category1' : category1,
                              'kids_items' : kids_items,
                              'search_field' : search_field,
                              'show_paginator':paginator.num_pages>1,
                              'has_prev':kids_items.has_previous(),
                              'has_next':kids_items.has_next(),
                              'page':page,
                              'pages':paginator.num_pages,
                              'next_page':page+1, 
                              'prev_page':page-1,
                              'has_prev10':has_prev10,
                              'has_next10':has_next10,
                              'prev_page10':prev_page10,
                              'next_page10':next_page10,
                              })
    return render_to_response('search.html', context)


def add(request):
    kid_titles = request.POST.getlist('kid_title')
    kid_urls = request.POST.getlist('kid_url')
    kid_images = request.POST.getlist('kid_image')
    checks = request.POST.getlist('check')
    cat2 = request.POST['category2']
    category2 = get_object_or_404(Category2,title=cat2)
    
    count = 0
    print checks
    print kid_titles
    print kid_urls
    
    for check in checks:
        if check:
            kid_title = kid_titles[count]
            kid_url = kid_urls[count]
            kid_image = kid_images[count]
            #print kid_title
            kid_item = Kid(title = kid_title, url = kid_url, image_url = kid_image, category = category2)
            kid_item.save()
        count = count + 1
    return HttpResponseRedirect('/schedule')


# user


def contact(request):
    category1 = Category1.objects.order_by('title')
    context = RequestContext(request,
                             {'category1' : category1
                              })
    return render_to_response('contact.html', context)    


def register_success(request):
    return render_to_response('registration/register_success.html',RequestContext(request))

def login_page(request):
    logout(request)
    username = password = ''

    if request.GET:
        print request.GET.get('next','/')
        next_page=request.GET.get('next','/')
        
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next_page = request.POST.get('next', '/')
                print next_page
                return HttpResponseRedirect(next_page)

    category1 = Category1.objects.order_by('title')
    context = RequestContext(request,
                             {'category1' : category1
                              })
                              
    return render_to_response('registration/login.html', context_instance=context)

def logout_page(request):
    #logout(request)
    return HttpResponseRedirect('/login')

def register_page(request):
    if request.POST:
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user=User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
                
            return HttpResponseRedirect('/register/success/')
    else:
        form=RegistrationForm()
            
    temp_param='Register'
    category1 = Category1.objects.order_by('title')
    user_param={'form':form,'temp_param':temp_param, 'category1' : category1}
    return render_to_response('registration/register.html',RequestContext(request,user_param))

@login_required(login_url=login_url)
def change_password(request):
    if request.POST:
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = PasswordChangeForm(None) 
    temp_param='Change Password'
    user_param={'form':form,'temp_param':temp_param}
    return render_to_response('form_template.html',RequestContext(request,user_param))

def reset_password(request):
    if request.POST:
        form=PasswordResetForm(data=request.POST)
        if form.is_valid():
            form.save(subject_template_name='registration/reset_subject.txt',
                      email_template_name='registration/reset_email.html',)
            return render(request,'registration/mail_send.html')
    else:
        form=PasswordResetForm()
    temp_param='Reset Password'
    category1 = Category1.objects.order_by('title')
    user_param={'form':form,'temp_param':temp_param,'category1' : category1}
    return render(request,'registration/reset.html',RequestContext(request,user_param))

@login_required(login_url=login_url)
def user_profile_view(request):
    temp_param='Change Profile'
    if request.user:
        form=ViewUserProfile(instance=request.user)
        
    if request.POST:
        form=ViewUserProfile(request.POST,instance=request.user)
        if form.is_valid():
            form.save()

    user_param={'form':form,'temp_param':temp_param}
    return render(request,'form_template.html',RequestContext(request,user_param))


def page_not_found_view(request):
    return render(request,'page_not_found.html',RequestContext(request))