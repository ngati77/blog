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
    url             = models.CharField(max_length=200, unique=True)
    title           = models.CharField(max_length=200)
    text            = models.TextField()
    created_date    = models.DateTimeField(default=timezone.now)
    image           = models.ImageField(blank = True, null = True, upload_to = 'Post/%Y/%m/')
    published_date  = models.DateTimeField(blank=True, null=True)
    has_group      = models.BooleanField(default=False)
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
    
    def get_next_pharse_number(self):
        queryPhrase = self.phrases.all().order_by('-order')
        if queryPhrase.exists():
            return (queryPhrase[0].order + 2)
        else: 
            return 0

    

class Phrase(models.Model):
    
    post            = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='phrases')
    title           = models.CharField(max_length=200,blank = True, null = True)
    text1_html_style  = models.BooleanField(default=False)
    text1           = models.TextField(blank = True, null = True)
    image           = models.ImageField(blank = True, null = True, upload_to = 'Phrase/%Y/%m/')
    image_sub       = models.CharField(max_length=200,blank = True, null = True)
    image2          = models.ImageField(blank = True, null = True, upload_to = 'Phrase/%Y/%m/')
    image2_sub      = models.CharField(max_length=200,blank = True, null = True)
    image3          = models.ImageField(blank = True, null = True, upload_to = 'Phrase/%Y/%m/')    
    image3_sub      = models.CharField(max_length=200,blank = True, null = True)
    order           = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        if not self.title:
            return (str(self.post) +  "-" + str(self.order))
        else:
            return (str(self.post) + "-" + self.title + "-" + str(self.order))
    def num_images(self):
        im1 = 1 if (self.image) else 0
        im2 = 1 if (self.image2) else 0
        im3 = 1 if (self.image3) else 0
        return str(im1 + im2 + im3)
    
class Comment(models.Model):
    post    = models.ForeignKey('blog.Post', on_delete=models.CASCADE, blank=True, null=True, related_name='comments')
    commentParent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='subComments')

    author = models.CharField(max_length=200)
    email  = models.EmailField(blank=True, null=True, default="")

    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

class Subscribed(models.Model):

    first_name       = models.CharField(max_length=200)
    email            = models.EmailField(blank=True, default="")
    confirmed        = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email