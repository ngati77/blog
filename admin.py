from django.contrib import admin

# Register your models here.
from .models import Post, Comment, Phrase, Subscribed

class PhraseInline(admin.TabularInline):
    model = Phrase
    extra = 3
    
class PostAdmin(admin.ModelAdmin):
    inlines         = [PhraseInline]
    
admin.site.register(Post,PostAdmin)
admin.site.register(Comment)
admin.site.register(Phrase)
admin.site.register(Subscribed)
