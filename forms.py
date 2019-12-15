# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 23:04:42 2019

@author: Tamuz
"""

from django import forms

from .models import Post, Comment, Phrase, Subscribed


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'image','type')
        

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)
        labels = {
        "author": "שם ",
        "text": "הערה"
    }


class PhraseForm(forms.ModelForm):

    class Meta:
        model = Phrase
        fields = ('title','text1_html_style','text1',
                  'image_num', 'image', 'image2', 'image3', 
                  'order')

class SubscribedForm(forms.ModelForm):

    class Meta:
        model = Subscribed
        fields = ('first_name', 'last_name','email')
        labels = {
        "first_name": "שם פרטי",
        "last_name": "שם משפחה",
        "email": "אמייל"
    }

                  

    