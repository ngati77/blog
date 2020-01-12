# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 19:59:27 2019

@author: Tamuz
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from datetime import datetime


from blog.models import Post


class BlogsPagesSitemap(Sitemap):
        
    def items(self):
        return ['blog:post_list']
    
    def changefreq(self, obj):
        return 'weekly'
    
    def lastmod(self, obj):
        return datetime.now()
    
    def location(self, obj):
        return reverse(obj)
    
class BlogsSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Post.objects.filter(published_date__isnull=False)

    def lastmod(self, obj):
        return datetime.now()
    
    def location(self, obj):
        return '/blog/post/' + str(obj.pk)  
        