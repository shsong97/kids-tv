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


def home(request):
    category1 = Category1.objects.order_by('title')
    kids_items = Kid.objects.order_by('-update_date')[:10]
    context = RequestContext(request,
                             {'category1': category1,
                              'kids_items': kids_items,
                              })
    return render_to_response('index.html', context)

def category1(request, cat_name1):
    category1 = Category1.objects.order_by('title')
    kids_items = Kid.objects.order_by('-update_date')[:10]
    context = RequestContext(request,
                             {'category1': category1,
                              'kids_items': kids_items,
                              })
    return render_to_response('index.html', context)

def category2(request, cat_name1, cat_name2):
    category1 = Category1.objects.order_by('title')
    kids_items = Kid.objects.order_by('-update_date')[:10]
    context = RequestContext(request,
                             {'category1': category1,
                              'kids_items': kids_items,
                              })
    return render_to_response('index.html', context)