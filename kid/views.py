# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils.translation import gettext as _
from django.utils.http import urlquote
from django.template import RequestContext

from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import *
from django.contrib.auth.decorators import login_required

from django.shortcuts import render,render_to_response, redirect,get_object_or_404

from django.core.paginator import Paginator
from django.db.models import Q

from kid.models import *
from kid.forms import *

from django.contrib.auth.decorators import permission_required, login_required
from django.http import JsonResponse
from datetime import datetime

login_url='/login'
ITEMS_PER_PAGE=10
PAGE_COUNT = 10

def home(request, cat_name1='All', cat_name2=''):
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
        next_page10 = (( page + PAGE_COUNT ) // PAGE_COUNT) * PAGE_COUNT + 1

    if page > PAGE_COUNT:
        has_prev10 = True
        prev_page10 = (( page - PAGE_COUNT ) // PAGE_COUNT) * PAGE_COUNT + 1

    from_page = ( page // PAGE_COUNT ) * PAGE_COUNT + 1
    

    if from_page + PAGE_COUNT < total_page:
        page_size = PAGE_COUNT
    else:
        page_size = total_page - from_page + 1

    for i in range(page_size):
        page_list.append((i+from_page))

    context = {  'category1': category1,
               'kids_items': kids_items,
               'cat_name1' : cat_name1,
               'cat_name2' : cat_name2,
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
              }
    return render(request,'search.html', context)

@permission_required('kid.add_kid')
def schedule(request):
    search_field = ''
    if 'search_field' in request.GET:
        if request.GET['search_field'] is not None:
            search_field=request.GET['search_field']

    page = '1'
    if 'page' in request.GET:
        if request.GET['page'] is not None:
            page=request.GET['page']

    page_url = '&page=' + page

    category1 = Category1.objects.order_by('title')
    category2 = Category2.objects.order_by('title')

    from bs4 import BeautifulSoup
    import urllib
    import sys

    if sys.version_info[0] == 3:
        from urllib.request import urlopen
    else:
        # Not Python 3 - today, it is most likely to be Python 2
        # But note that this might need an update when Python 4
        # might be around one day
        from urllib import urlopen

    kids_items = []
    if search_field != '':
        youtube_url ='https://www.youtube.com'
        url = youtube_url + '/results?search_query=' + urlquote(search_field) + page_url
        
        html_doc = urllib.urlopen(url)

        soup = BeautifulSoup(html_doc, "html.parser")
        links = soup.findAll('div', attrs={'class':'yt-lockup-dismissable'})

        item_id = 0
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

            kids_items.append(( item_id, title, h_url, image_url ))
            item_id += 1

    context = {'category1' : category1,
               'category2' : category2,
               'kids_items' : kids_items,
               'search_field' : search_field,
               'page' : page,
              }
    return render(request, 'schedule.html', context)

def search(request):
    category1 = Category1.objects.order_by('title')
    search_field = ''
    if 'search_field' in request.GET:
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

    page_list = []
    has_prev10=False
    has_next10=False
    prev_page10=0
    next_page10=0
    from_page=0
    total_page = paginator.num_pages
    if total_page > PAGE_COUNT and page + PAGE_COUNT < total_page:
        has_next10 = True
        next_page10 = (( page + PAGE_COUNT ) // PAGE_COUNT) * PAGE_COUNT + 1

    if page > PAGE_COUNT:
        has_prev10 = True
        prev_page10 = (( page - PAGE_COUNT ) // PAGE_COUNT) * PAGE_COUNT + 1

    from_page = int( page // PAGE_COUNT ) * PAGE_COUNT + 1

    if from_page + PAGE_COUNT < total_page:
        page_size = PAGE_COUNT
    else:
        page_size = total_page - from_page + 1

    page_size = int(page_size)

    for i in range(page_size):
        page_list.append((i+from_page))

    context = {'category1' : category1,
               'kids_items' : kids_items,
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
              }
    return render(request, 'search.html', context)


def add(request):
    '''
    search youtube and add youtube url
    '''
    kid_titles = request.POST.getlist('kid_title')
    kid_urls = request.POST.getlist('kid_url')
    kid_images = request.POST.getlist('kid_image')
    checks = request.POST.getlist('check')
    checks = request.POST.getlist('check')
    cat2 = request.POST['category2']
    category2 = get_object_or_404(Category2,title=cat2)

    for check in checks:
        if check:
            id = int(check)
            kid_title = kid_titles[id]
            kid_url = kid_urls[id]
            kid_image = kid_images[id]
            youtube_id = kid_urls[id].split('?')[1][2:]
            kid_item = Kid(title = kid_title, url = kid_url, image_url = kid_image, 
                category = category2, youtube_id = youtube_id)
            kid_item.save()

    if request.META['HTTP_REFERER']:
        url = request.META['HTTP_REFERER']
    else:
        url='/schedule'

    return HttpResponseRedirect(url)

@login_required(login_url=login_url)
def delete(request, kid_id):
    kid_item = get_object_or_404(Kid,id=kid_id)
    if request.user.is_staff:
        kid_item.delete()

    if request.META['HTTP_REFERER']:
        if 'detail' in request.META['HTTP_REFERER']:
          url = '/'
        else:
          url = request.META['HTTP_REFERER']
    else:
        url='/'

    return HttpResponseRedirect(url)

def detail(request, kid_id):
    kid_item = get_object_or_404(Kid,id=kid_id)
    like_count = Favorite.objects.filter(fav_kid=kid_item).count()
    kid_user = KidUser.objects.get(kid_user=request.user)
    my_click = False
    try:
        favorite = Favorite.objects.get(fav_kid=kid_item, fav_user=kid_user)
        my_click = True
    except:
        favorite = None
    category1 = Category1.objects.order_by('title')

    return render(request,'detail.html', {
        'category1' : category1, 
        'kid' : kid_item, 
        'like_count': like_count,
        'my_click' : my_click})

@login_required(login_url=login_url)
def detail_like(request, kid_id):
    kid_user = KidUser.objects.get(kid_user=request.user)
    fav_kid = Kid.objects.get(id=kid_id)
    my_click = False
    try:
        favorite = Favorite.objects.get(fav_kid=fav_kid, fav_user=kid_user)
        my_click = True
    except:
        favorite = None

    if favorite:
        favorite.delete()
    else:
        Favorite.objects.create(fav_kid=fav_kid, fav_user=kid_user)
    like_count=Favorite.objects.filter(fav_kid=kid_id).count()
    data_dict={'like_count':like_count, 'my_click' : my_click}
    return JsonResponse(data_dict)

def detail_favorite(request, kid_id):
    try:
        fav_kid = Kid.objects.get(id=kid_id)
        favorites = Favorite.objects.filter(fav_kid=fav_kid)        
    except:
        favorites = None

    return JsonResponse({'favorites':favorites})

def contact(request):
    category1 = Category1.objects.order_by('title')
    return render(request,'contact.html', {'category1' : category1})


def register_success(request):
    return render(request,'registration/register_success.html')

def login_page(request):
    logout(request)
    username = password = ''

    if request.GET:
        next_page=request.GET.get('next','/')

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next_page = request.POST.get('next', '/')
                return HttpResponseRedirect(next_page)

    category1 = Category1.objects.order_by('title')
    return render(request,'registration/login.html', {'category1' : category1})

def logout_page(request):
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
            kid_user = KidUser.objects.create(kid_user=user,
                invalid_password_count=0,address='',last_login_date=datetime.today())
            return HttpResponseRedirect('/register/success/')
    else:
        form=RegistrationForm()

    temp_param='Register'
    category1 = Category1.objects.order_by('title')
    user_param={'form':form,'temp_param':temp_param, 'category1' : category1}
    return render(request,'registration/reg_form_template.html',user_param)

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
    return render(request,'registration/reg_form_template.html',user_param)

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
    return render(request,'registration/reg_form_template.html',user_param)

@login_required(login_url=login_url)
def user_profile_view(request):
    temp_param='Change Profile'
    if request.user:
        kid_user = KidUser.objects.get(kid_user=request.user)
        form=ViewUserProfile(instance=kid_user)

    if request.POST:
        kid_user = KidUser.objects.get(kid_user=request.user)
        form=ViewUserProfile(request.POST,instance=kid_user)
        if form.is_valid():
            form.save()

    user_param={'form':form,'temp_param':temp_param}
    return render(request,'registration/reg_form_template.html',user_param)


def page_not_found_view(request):
    return render(request,'page_not_found.html')

