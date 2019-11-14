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
        fields = ('title', 'text',)
        

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

class PhraseForm(forms.ModelForm):

    class Meta:
        model = Phrase
        fields = ('title_checkbox', 'title','text1_checkbox','text1_html_style','text1','image_checkbox','image','text2_checkbox','text2_html_style','text2','order')

    