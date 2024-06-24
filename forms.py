# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 23:04:42 2019

@author: Tamuz
"""

from django import forms
from django.forms import ModelForm, Textarea

from .models import Post, Comment, Phrase, Subscribed

from django_recaptcha.fields import ReCaptchaField


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'url', 'image','type')
        

class CommentForm(forms.ModelForm):
    #captcha = ReCaptchaField(public_key=RECAPTCHA_PUBLIC_KEY, private_key=RECAPTCHA_PRIVATE_KEY)
    class Meta:
        model = Comment
        fields = ('author','email' ,'text')
        labels = {
        "author": "",
        "text": "",
        "email": ""
        }
        widgets = {
            'author':   Textarea(attrs={'placeholder': 'שם','cols': 10, 'rows': 1}),
            'text':   Textarea(attrs={'placeholder': 'כיתבו כאן את הערה','cols': 40, 'rows': 5}),
            'email':   Textarea(attrs={'placeholder': 'דואר אלקטרוני','cols': 40, 'rows': 5}),
        }


class PhraseForm(forms.ModelForm):

    class Meta:
        model = Phrase
        fields = ('title','text1_html_style','text1',
                   'image','image_sub', 'image2', 'image2_sub','image3','image3_sub', 
                  'order')
        labels = {
        "title":  'פוסט כותרת',
        "text1": 'טקסט',
        "image_sub": 'טקסט תמונה 1',
        "image2_sub":'טקסט תמונה 2',
        "image3_sub":'טקסט תמונה 3',
        "order":'מיקום הפסקה',
        }
        widgets = {
            'title':   Textarea(attrs={'placeholder': 'פוסט כותרת','cols': 70, 'rows': 2}),
            'text1':   Textarea(attrs={'placeholder': 'טקסט','cols': 70, 'rows': 20}),
            'image_sub':   Textarea(attrs={'placeholder': 'טקסט תמונה 1','cols': 70, 'rows': 2}),
            'image2_sub':   Textarea(attrs={'placeholder': 'טקסט תמונה 2','cols': 70, 'rows': 2}),
            'image3_sub':   Textarea(attrs={'placeholder': 'טקסט תמונה 3','cols': 70, 'rows': 2}),
        }

class SubscribedForm(forms.ModelForm):

    class Meta:
        model = Subscribed
        fields = ('first_name','email')
        labels = {
        "first_name": "",
        "email": "",
        }
        widgets = {
            'first_name':   Textarea(attrs={'placeholder': 'שם פרטי','cols': 20, 'rows': 1}),
            'email':        Textarea(attrs={'placeholder': 'דוא"ל','cols': 20, 'rows': 1}),
        }
    

    
