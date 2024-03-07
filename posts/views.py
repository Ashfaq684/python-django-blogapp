from django.shortcuts import get_object_or_404, render, redirect
from .forms import PostForm, CommentForm
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.text import slugify
from .models import Comments, Post, Tag
from django.contrib.auth.models import User
from django.db.models import Count

# Create your views here.

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            base_slug = slugify(post.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            post.slug = slug
            post.save()
            return redirect('post_page', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def update_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user != post.author:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_page', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/edit_post.html', {'form': form})


@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user != post.author:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    if request.method == 'POST':
        post.delete()
        return redirect('profile')
    return render(request, 'posts/delete_post.html', {'post': post})


def post_page(request, slug):
    post = Post.objects.get(slug = slug)
    comments = Comments.objects.filter(post=post, parent=None)
    form = CommentForm()
    comment_count = comments.count()
    # Bookmark logic
    bookmarked = False
    if post.bookmarks.filter(id = request.user.id).exists():
        bookmarked = True
    is_bookmarked = bookmarked
    
    # Liked logic
    liked = False
    if post.likes.filter(id = request.user.id).exists():
        liked = True
    number_of_likes = post.number_of_likes()
    is_liked = liked
    
    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_obj = None
            if request.POST.get('parent'):
                parent = request.POST.get('parent')
                parent_obj = Comments.objects.get(id=parent)
                if parent_obj:
                    comment_reply = comment_form.save(commit=False)
                    comment_reply.parent = parent_obj
                    comment_reply.post = post
                    comment_reply.save()
                    return HttpResponseRedirect(reverse('post_page', kwargs={'slug':slug})) 
            else:
                comment = comment_form.save(commit=False)
                postid = request.POST.get('post_id')
                post = Post.objects.get(id = postid)
                comment.post = post
                comment.save()
                return HttpResponseRedirect(reverse('post_page', kwargs={'slug':slug}))
            
    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count = post.view_count + 1
    post.save()
    
    # sidebar
    recent_posts = Post.objects.exclude(id=post.id).order_by('-last_updated')[0:2]
    top_authors = User.objects.annotate(number = Count('post')).order_by('-number')[0:2]
    tags = Tag.objects.all()
    related_posts = Post.objects.exclude(id=post.id).filter(author=post.author)[0:2]
    
    context = {
        'post':post, 
        'form':form, 
        'comments':comments, 
        'is_bookmarked':is_bookmarked, 
        'is_liked':is_liked, 
        'number_of_likes':number_of_likes, 
        'recent_posts':recent_posts, 
        'top_authors':top_authors, 
        'tags':tags, 
        'related_posts':related_posts,
        'comment_count':comment_count,
    }
    
    return render(request, 'posts/post.html', context)

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    top_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-view_count')[0:2]
    recent_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-last_updated')[0:2]
    tags = Tag.objects.all()
    
    context = {
        'tag':tag, 
        'top_posts':top_posts, 
        'recent_posts':recent_posts, 
        'tags':tags
    }
    return render(request, 'posts/tag.html', context)


def bookmark_post(request, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.bookmarks.filter(id = request.user.id).exists():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)
    return HttpResponseRedirect(reverse('post_page', args=[str(slug)]))


def like_post(request, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id = request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_page', args=[str(slug)]))


def all_bookmarked_posts(request):
    all_bookmarked_posts = Post.objects.filter(bookmarks=request.user)
    
    context={
        'all_bookmarked_posts':all_bookmarked_posts
    }
    
    return render(request, 'posts/all_bookmarked_posts.html', context)


def all_liked_posts(request):
    all_liked_posts = Post.objects.filter(likes=request.user)
    
    context={
        'all_liked_posts':all_liked_posts
    }
    
    return render(request, 'posts/all_liked_posts.html', context)