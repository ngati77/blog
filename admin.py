from django.contrib import admin

# Register your models here.
from .models import Post, Comment, Phrase, Subscribed
from django.template.loader import render_to_string
from tours.tour_emails import tour_emails
from django.conf import settings

class PhraseInline(admin.TabularInline):
    model = Phrase
    extra = 3
    




class PostAdmin(admin.ModelAdmin):
    inlines         = [PhraseInline]
    actions         = ['send post']

    def send_post_email(self, request, queryset):
        ''' Send email to subscribed list
        '''
        for post in queryset:
            subList = Subscribed.objects.filter(confirmed=True)
            title   = post.text
            msg_plain =  "בלוג חדש"

            for subscribed in subList:
                to=[subscribed.email]
                msg_html = render_to_string('emails/new_post.html',{'post':post, 'subscribed':subscribed })
                print(msg_html)
                #emailTitle = " בדוק בלוג "
                tour_emails.send_email(to=to,
                                    msg_html=msg_html, 
                                    msg_plain=msg_plain, 
                                    cc=settings.BCC_EMAIL, 
                                    title=title)
    send_post_email.short_description    = "Sending post to subscribed list"
    actions = [send_post_email]


admin.site.register(Post,PostAdmin)
admin.site.register(Comment)
admin.site.register(Phrase)
admin.site.register(Subscribed)
