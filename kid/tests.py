# -*- coding: utf-8 -*-
import datetime
from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse
from kid.models import Category1, Category2, Kid

# Create your tests here.
def create_category(self,title):
	return Category1.objects.create(title=title)


def create_category_sub(self, title, bit_title):
	cat1=get_object_or_404(Category1,title=big_title)
	return Category2.objects.create(title=title, parent_category=cat1)


def create_kid(title, sub_title):
	cat2=get_object_or_404(Category2, title=sub_title)
	url = "http://test.com"
	image_url = "http://image.url.com"
	return Kid.objects.create(title=title, url=url, image_url=image_url, category=cat2)	


# user test case
class UserTestCase(TestCase):
	def login_test(self):
		response = self.client.get('/login')
		self.assertEqual(response.status_code, 200)


	def logout_test(self):
		response = self.client.get('/logout')
		print response
		self.assertEqual(response.status_code, 209)


class KidTestCase(TestCase):
	def create_kid_test(self, title):
		create_category("cat1")
		create_category_sub("cat2", "cat1")
		create_kid("title","cat2")
		self.assertEqual(response.status_code, 200)
