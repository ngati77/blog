from django.contrib import admin

# Register your models here.
from .models import Post, Comment, Phrase




class PhraseInline(admin.TabularInline):
    model = Phrase
    extra = 3
    
class PhraseAdmin(admin.ModelAdmin):
            
    fieldsets = [
        
        ('Date information', {'fields': ['trip_date']}),
        (None,               {'fields': ['post']}),
        (None,               {'fields': ['title_checkbox']}),
        (None,               {'fields': ['title']}),
        (None,               {'fields': ['image_checkbox']}),
        (None,               {'fields': ['image']}),
        (None,               {'fields': ['text1_checkbox']}),
        (None,               {'fields': ['text1']}),
        (None,               {'fields': ['text2_checkbox']}),
        (None,               {'fields': ['text2']}),
        (None,               {'fields': ['image_checkbox']}),
        (None,               {'fields': ['image']}),
        (None,               {'fields': ['order']}),
       
    ]
    
class PostAdmin(admin.ModelAdmin):
    inlines         = [PhraseInline]
    
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Phrase)
