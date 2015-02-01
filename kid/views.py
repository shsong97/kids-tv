# -*- encoding:utf-8 -*-

from django.http import HttpResponse, Http404
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.translation import gettext as _

from kid.models import *


def home(request, cat_name1='All', cat_name2=''):
    name=cat_name1+'/'+cat_name2
    category1 = Category1.objects.order_by('title')
    if cat_name2 != '':
        cat2=get_object_or_404(Category2,title=cat_name2)
        kids_items=cat2.kid_set.order_by('-update_date')[:10]
    else:
        kids_items = Kid.objects.order_by('-update_date')[:10]
        
    context = RequestContext(request,
                             {'category1': category1,
                              'kids_items': kids_items,
							  'name' : name,
                              })
    return render_to_response('index.html', context)


def schedule(request):
    search_url = 'https://www.youtube.com/results?search_query='
    search_title = ''
    if request.GET.has_key('search_field'):
        if request.GET['search_field'] is not None:
            search_title=request.GET['search_field']
    
    from bs4 import BeautifulSoup
    import urllib

    youtube_url ='https://www.youtube.com'
    url = youtube_url + '/results?search_query=' + search_title.encode('utf-8')
    html_doc = urllib.urlopen(url)
    soup = BeautifulSoup(html_doc)
    links = soup.findAll('div', attrs={'class':'yt-lockup-dismissable'})

    kids_items = []
    
    if search_title != '':
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

    category1 = Category1.objects.order_by('title')
    context = RequestContext(request,
                             {'category1' : category1,
                              'kids_items' : kids_items,
                              })
    return render_to_response('schedule.html', context)

def search(request):
    category1 = Category1.objects.order_by('title')
    search_field = ''
    if request.GET.has_key('search_field'):
        if request.GET['search_field'] is not None:
            search_field = request.GET['search_field']
            kids_items = Kid.objects.filter(title__icontains=search_field).order_by('-update_date')[:10]
    else:
        kids_items = Kid.objects.order_by('-update_date')[:10]
    
    context = RequestContext(request,
                             {'category1' : category1,
                              'kids_items' : kids_items,
                              'search_field' : search_field
                              })
    return render_to_response('search.html', context)
