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
        fields = ('title', 'text', 'image',)
        

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

class PhraseForm(forms.ModelForm):

    class Meta:
        model = Phrase
        fields = ('title','text1_html_style','text1',
                  'image_checkbox', 'image_num', 'image', 'image2', 'image3', 
                  'text2_html_style', 'text2', 'order')

    