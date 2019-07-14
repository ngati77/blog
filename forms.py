# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 23:04:42 2019

@author: Tamuz
"""

from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)
        

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)