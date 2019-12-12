# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 23:04:42 2019

@author: Tamuz
"""

from django import forms

from .models import Post, Comment, Phrase


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'image','type')
        

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

class PhraseForm(forms.ModelForm):

    class Meta:
        model = Phrase
        fields = ('title','text1_html_style','text1',
                  'image_num', 'image', 'image2', 'image3', 
                  'order')

    