# -*- coding: utf-8 -*-
import datetime
from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse
from kid.models import Category1, Category2, Kid, KidUser, Favorite
from django.shortcuts import render,render_to_response, redirect,get_object_or_404
from django.core.exceptions import *
from django.contrib.auth.models import User

# Create your tests here.
def create_category(title):
    return Category1.objects.create(title=title)


def create_category_sub(title, big_title):
    cat1=get_object_or_404(Category1,title=big_title)
    return Category2.objects.create(title=title, parent_category=cat1)


def create_kid(title, sub_title):
    cat2=get_object_or_404(Category2, title=sub_title)
    url = "http://test.com"
    image_url = "http://image.url.com"
    return Kid.objects.create(title=title, url=url, image_url=image_url, category=cat2) 

def create_kid_user(username, email, password):
    user = User.objects.create_user(username=username, email=email, password=password)
    kid_user = KidUser.objects.create(kid_user=user)
    return kid_user

class KidTestCase(TestCase):
    kid_user1 = None
    def setUp(self):
        create_category("cat1")
        create_category_sub("cat2", "cat1")
        create_category_sub("cat3", "cat1")
        self.user = User.objects.create_superuser('testuser','test@domain.com','test1234')
        self.client.login(username='testuser',password='test1234')
        self.kid_user1 = KidUser.objects.create(kid_user=self.user)
        kid_item = create_kid("kid_item","cat2")
        Favorite.objects.create(fav_kid=kid_item, fav_user=self.kid_user1)
        for i in range(100):
            create_kid_user(username='test_user'+str(i), email='testuser'+str(i)+'@domain.com', password='passwd'+str(i))
            create_kid('title'+str(i),'cat2')

    def create_kid_test(self):
        create_kid("create_kid_item","cat2")
        kid = Kid.objects.get(title="create_kid_item")
        self.assertNotEqual(kid,None)
        self.assertTrue(isinstance(kid,Kid))

    def delete_kid_test(self):
        kid = Kid.objects.get(title="title1")
        kid.delete()
        exception = False
        with self.assertRaises(ObjectDoesNotExist, None) as cm:
            kid2 = Kid.objects.get(title="title1")
        the_exception = cm.exception
        # self.assertEqual(the_exception.error,'error')

    def delete_kid_request_test(self):
        self.client.login(username='test_user',password='test1234')
        response = self.client.get('/delete/1') # 301 move permanantly
        self.assertEqual(response.status_code, 301)

    def home_test(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def pagination_min_test(self):
        response = self.client.get('/?page=1')
        self.assertEqual(response.status_code, 200)

    def pagination_error_test(self):
        response = self.client.get('/?page=30')
        self.assertEqual(response.status_code, 200)

    def pagination_max_test(self):
        response = self.client.get('/?page=20')
        self.assertEqual(response.status_code, 200)

    def pagination_nextpage_test(self):
        response = self.client.get('/?page=7')
        self.assertEqual(response.status_code, 200)

    def schedule_test(self):
        response = self.client.get('/schedule')
        self.assertEqual(response.status_code, 301)

    def schedule_field_test(self):
        response = self.client.get('/schedule/?search_field=test')
        self.assertEqual(response.status_code, 302)

    def search_test(self):
        response = self.client.get('/search')
        self.assertEqual(response.status_code, 301)

    def search_keyword_test(self):
        response = self.client.get('/search/?search_field=title')
        self.assertEqual(response.status_code, 200)

    def add_test(self):
        response = self.client.get('/add')
        self.assertEqual(response.status_code, 301)

    def watch_cat1_test(self):
        response = self.client.get('/watch/cat1/')
        self.assertEqual(response.status_code, 200)

    def watch_cat2_test(self):
        response = self.client.get('/watch/cat1/cat2/')
        self.assertEqual(response.status_code, 200)

    def detail_test(self):
        self.client.login(username='testuser',password='test1234')

        response = self.client.get('/detail/1/')
        self.assertEqual(response.status_code, 200)

    def detail_like_test(self):
        self.client.login(username='testuser',password='test1234')
        response = self.client.get('/detail/1/like/')
        self.assertEqual(response.status_code, 302)

    def contact_test(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

    def detail_favorite_test(self):
        self.client.login(username='testuser',password='test1234')
        fav_user = KidUser.objects.get(kid_user=self.user)
        favor = Favorite.objects.get(fav_user=fav_user)
        favor_id = favor.pk
        response = self.client.get('/detail/'+str(favor_id)+'/favorite/')
        self.assertEqual(response.status_code, 200)

    def myfavorite_test(self):
        response = self.client.get('/myfavorite/')
        self.assertEqual(response.status_code, 302)

    def mydelete_test(self):
        self.client.login(username='testuser',password='test1234')
        response = self.client.get('/mydelete/1/')
        self.assertEqual(response.status_code, 200)

    def delete_test(self):
        self.client.login(username='testuser',password='test1234')
        response = self.client.get('/delete/1/')
        self.assertEqual(response.status_code, 200)

    def login_page_test(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def login_page_post_test(self):
        login_bool = self.client.login(username='testuser',password='test1234')
        self.assertTrue(login_bool)

    def logout_test(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302) # 302 redirect

    def admin_page_test(self):
        self.client.login(username='testuser',password='test1234')
        response = self.client.get('/admin/')
        self.assertNotEqual(response.status_code, 404)
        self.assertNotEqual(response.status_code, 500)

    def feed_page_test(self):
        response = self.client.get('/feed/')
        self.assertNotEqual(response.status_code, 404)
        self.assertNotEqual(response.status_code, 500)

    def profile_page_test(self):
        response = self.client.get('/profile/')
        self.assertNotEqual(response.status_code, 404)
        self.assertNotEqual(response.status_code, 500)

        response = self.client.post('/profile/', data={'kid_user':self.kid_user1})
        self.assertNotEqual(response.status_code, 404)
        self.assertNotEqual(response.status_code, 500)

    def register_test(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/register/',
            {'username':'test1','password1':'testpassword','email':'test@domain.com'})

        self.assertEqual(response.status_code, 200)

    def change_password_test(self):
        login_bool = self.client.login(username='testuser',password='test1234')
        self.assertEqual(login_bool, True)

        response = self.client.get('/changepassword/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/changepassword/', 
            {'old_password':'oldpassword',
            'new_password1':'new_password',
            'new_password2':'new_password'})
        self.assertEqual(response.status_code, 200)

