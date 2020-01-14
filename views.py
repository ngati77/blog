from django.shortcuts import render,  get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment, Phrase
from .forms import PostForm, CommentForm, PhraseForm, SubscribedForm
from tours.tour_emails import tour_emails
from django.conf import settings
from django.template.loader import render_to_string



from django.contrib.auth.decorators import login_required, user_passes_test

''' Check if user has permition to edit blog'''
def group_required(*group_names):
   """Requires user membership in at least one of the groups passed in."""

   def in_groups(u):
       if u.is_authenticated:
           if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
               return True
       return False
   return user_passes_test(in_groups)

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now(),type='p').order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': [posts[0::2], posts[1::2]],'page_title':'האחרונים שלנו'})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post, 'page_title':post.title,'ShowComments':True})

@login_required
# The way to use this decorator is:
@group_required('blog_admin')
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
@group_required('blog_admin')
def phrase_new(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PhraseForm(request.POST, request.FILES)
        if form.is_valid():
            phrase = form.save(commit=False)
            phrase.post = post
            phrase.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        next_order = post.get_next_pharse_number()
        form = PhraseForm(initial={'order': next_order})
    return render(request, 'blog/phrase_edit.html', {'form': form})

@login_required
@group_required('blog_admin')
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
@group_required('blog_admin')
def phrase_edit(request, pk):
    phrase = get_object_or_404(Phrase, pk=pk)
    if request.method == "POST":
        form = PhraseForm(request.POST, request.FILES,instance=phrase)
        if form.is_valid():
            phrase = form.save(commit=False)
            phrase.save()
            return redirect('blog:post_detail', pk=phrase.post.pk)
    else:
        form = PhraseForm(instance=phrase)
    return render(request, 'blog/phrase_edit.html', {'form': form})

@login_required
@group_required('blog_admin')
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_list.html', {'posts': [posts[0::2], posts[1::2]],'page_title':'טיוטות'})


@login_required
@group_required('blog_admin')
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post_detail', pk=pk)

@login_required
@group_required('blog_admin')
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog:post_list')

def post_writers(request):
    posts = Post.objects.filter(published_date__isnull=False,type='w').order_by('created_date')
    return render(request, 'blog/post_detail.html', {'post': posts[0],'page_title':'על הכותבים','ShowComments':False})

    # return render(request, 'blog/post_list.html', {'posts': [posts[0],'page_title':'קצת עלינו'})


def inform_admin(title):
    to=[settings.EMAIL_GMAIL_YAEL]
    
    msg_html = render_to_string('emails/email_admin.html')
    msg_plain =  "בדוק בלוג"
    #emailTitle = " בדוק בלוג "
    tour_emails.send_email(to=to,
                            msg_html=msg_html, 
                            msg_plain=msg_plain, 
                            cc=settings.BCC_EMAIL, 
                            title=title)

'''
def send_email(task, obj):
    to=[settings.EMAIL_GMAIL_YAEL]
    if obj.email:
        to.append(obj.email)
    if task == 'Check':
        msg_html = ""
        msg_plain =  "בדוק בלוג"
        emailTitle = " בדוק בלוג "
        to=settings.BCC_EMAIL
    if task=='New comment':
        msg_html = render_to_string('emails/email_new_comment.html', {'comment':obj})
        msg_plain = str(obj.id) + " הערה חדשה"
        emailTitle = "תודה שכתבת לנו"
    elif task = 'New Subscribed':
        msg_html = render_to_string('emails/email_new_subscribed.html', {'comment':obj})
        msg_plain = str(obj.id) + " משתמש חדש "
        emailTitle = "תודה שנרשמת"
    elif task = 'Published comment':
        # A new comment has been published, inform the person who wrote it
        if (obj.post):
            msg_html = render_to_string('emails/email_comment_published.html', {'comment':obj})
            msg_plain = str(obj.id) + "תגובה פורסמה "
            emailTitle = "התגובה שלך פורסמה"


        
try:

    tour_emails.send_email( to=[settings.EMAIL_GMAIL_YAEL],
                                    msg_html=msg_html, 
                                    msg_plain=msg_plain, 
                                    cc=[], 
                                    title=title)
except:
    print('Got an error...')
'''

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            inform_admin('new post comment')
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

def add_comment_to_comment(request, PostPk, CommentPk):
    commentParent = get_object_or_404(Comment, pk=CommentPk)
    #post = get_object_or_404(Post, pk=PostPk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.commentParent = commentParent
            comment.save()
            inform_admin('new comment to comment')

            return redirect('blog:post_detail', pk=PostPk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})
 
def subscribed_success(request):
    inform_admin('new subscribed')
    return render(request, 'blog/subscribed_success.html',{'page_title':'הרישום הצליח'})


def subscribed_view(request):
    if request.method == "POST":
        form = SubscribedForm(request.POST)
        if form.is_valid():
            subscribed = form.save(commit=False)
            subscribed.save()
            return redirect('blog:subscribed_success')
    else:
        form = SubscribedForm()
    return render(request, 'blog/subscribed.html', {'form': form})

@login_required
@group_required('blog_admin')
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    # If this is not null then it point to a post
    if (comment.post):
        return redirect('blog:post_detail', pk=comment.post.pk)
    else:
        return redirect('blog:post_detail', pk=comment.commentParent.post.pk)

@login_required
@group_required('blog_admin')
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('blog:post_detail', pk=comment.post.pk)