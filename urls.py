# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 22:23:09 2019

@author: Tamuz
"""

from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<str:url>', views.post_detail, name='post_detail'),
    path('failure/', views.failure, name='failure'),
    path('secure_post_detail/<str:url>', views.secure_post_detail, name='secure_post_detail'),
    path('post/new', views.post_new, name='post_new'),
    path('post/<int:pk>/edit', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('writers/', views.post_writers, name='post_writers'),
    path('post/<pk>/publish', views.post_publish, name='post_publish'),
    path('post/<pk>/remove', views.post_remove, name='post_remove'),
    path('post/<str:url>/comment', views.add_comment_to_post, name='add_comment_to_post'),
    path('post/<str:PostUrl>/<int:CommentPk>/comment', views.add_comment_to_comment, name='add_comment_to_comment'),
    path('comment/<int:pk>/approve', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove', views.comment_remove, name='comment_remove'),
    path('phrase/<int:pk>/edit', views.phrase_edit, name='phrase_edit'),
    path('phrase/<int:pk>/new', views.phrase_new, name='phrase_new'),
    
    path('subscribed/', views.subscribed_view, name='subscribed_view'),
    path('subscribed_success/', views.subscribed_success, name='subscribed_success'),


]