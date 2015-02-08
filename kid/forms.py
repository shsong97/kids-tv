# -*- encoding:utf-8 -*-
from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm

class ViewUserProfile(ModelForm):
    class Meta:
        model=User
        #fields = '__all__'
        fields = ['username', 'first_name','last_name','email',]
        
class RegistrationForm(forms.Form):
    username=forms.CharField(label='Username',max_length=30)
    email=forms.EmailField(label='Email')
    password1=forms.CharField(
        label='Password',
        widget=forms.PasswordInput()    
    )
    password2=forms.CharField(
        label='Password(confirm)',
        widget=forms.PasswordInput()
    )
    # clean_<field> : valid field
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1=self.cleaned_data['password1']
            password2=self.cleaned_data['password2']
            if password1==password2:
                return password2
        raise forms.ValidationError('password does not match')

    def clean_username(self):
        username=self.cleaned_data['username']
        if not re.search(r'\w+$',username):
            raise forms.ValidationError('user name allows charactor, number, underscore')
        
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('already exists username')

    def clean_email(self):
        email=self.cleaned_data['email']        
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('already exists email')
    