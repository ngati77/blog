from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class Post(models.Model):
    POST_TYPE = (
    ('p', 'Post'),
    ('w', 'Writer'),
    ('h', 'Home'),
)
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title           = models.CharField(max_length=200)
    text            = models.TextField()
    created_date    = models.DateTimeField(default=timezone.now)
    image           = models.ImageField(blank = True, null = True, upload_to = 'Post/%Y/%m/')
    published_date  = models.DateTimeField(blank=True, null=True)
    type = models.CharField(
            max_length=1, 
            choices=POST_TYPE,
            default='p',
    )

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)
    

class Phrase(models.Model):
    
    post            = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='phrases')
    title           = models.CharField(max_length=200,blank = True, null = True)
    text1_html_style  = models.BooleanField(default=False)
    text1           = models.TextField(blank = True, null = True)
    image_num       = models.IntegerField(default=1, blank=True, null=True)
    image           = models.ImageField(blank = True, null = True, upload_to = 'Phrase/%Y/%m/')
    image2          = models.ImageField(blank = True, null = True, upload_to = 'Phrase/%Y/%m/')
    image3          = models.ImageField(blank = True, null = True, upload_to = 'Phrase/%Y/%m/')    
    order           = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        if not self.title:
            return (str(self.post) +  "-" + str(self.order))
        else:
            return (str(self.post) + "-" + self.title + "-" + str(self.order))
    
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
    
   