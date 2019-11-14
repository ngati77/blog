from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class Post(models.Model):
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title           = models.CharField(max_length=200)
    text            = models.TextField()
    created_date    = models.DateTimeField(default=timezone.now)
    image           = models.ImageField(blank = True, null = True, upload_to = 'Post/%Y/%m/')
    published_date  = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)
    

class Phrase(models.Model):
    post            = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='phrases')
    title_checkbox  = models.BooleanField(default=False)
    title           = models.CharField(max_length=200)
    image_checkbox  = models.BooleanField(default=False)
    image           = models.ImageField(blank = True, null = True, upload_to = 'Post/%Y/%m/')
    text1_checkbox  = models.BooleanField(default=False)
    text1_html_style  = models.BooleanField(default=False)
    text1           = models.TextField()
    text2_checkbox  = models.BooleanField(default=False)
    text2_html_style  = models.BooleanField(default=False)
    text2           = models.TextField()
    order           = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return (str(self.post) + " " + str(self.order))
    
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
    
   