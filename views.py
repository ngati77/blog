from django.shortcuts import render,  get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment, Phrase
from .forms import PostForm, CommentForm, PhraseForm, SubscribedForm

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
        form = PhraseForm()
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

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

 
def subscribed_success(request):
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
    return redirect('blog:post_detail', pk=comment.post.pk)

@login_required
@group_required('blog_admin')
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('blog:post_detail', pk=comment.post.pk)