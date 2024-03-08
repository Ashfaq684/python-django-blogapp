from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from posts.models import Post, WebsiteMeta
from posts.forms import SubscribeForm
from accounts.models import Profile
from django.db.models import Q


def index(request):
    posts = Post.objects.all()
    top_posts = Post.objects.all().order_by('-view_count')[0:3]
    recent_posts = Post.objects.all().order_by('-last_updated')[0:3]
    featured_blog = Post.objects.filter(is_featured = True)
    subscribe_form = SubscribeForm()
    subscribe_successful = None
    website_info = None
    
    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]
        
    if featured_blog:
        featured_blog = featured_blog[0]
    
    if request.POST:
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            request.session['subscribed'] = True
            subscribe_successful = 'Subscribed Successfully'
            subscribe_form = SubscribeForm()
    
    profile = request.user.profile if hasattr(request.user, 'profile') else None
    
    context = {
        'posts':posts, 
        'website_info':website_info, 
        'top_posts':top_posts, 
        'recent_posts':recent_posts, 
        'subscribe_form':subscribe_form, 
        'subscribe_successful':subscribe_successful, 
        'featured_blog': featured_blog,
        'profile': profile,
    }
    
    return render(request, 'index.html', context)


def search_posts(request):
    search_query = request.GET.get('q', '')
    post_list = Post.objects.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query)
        )
    
    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'posts': posts,
        'search_query': search_query
    }
    
    return render(request, 'posts/search.html', context)


def about(request):
    website_info = None   
    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]
    
    context = {
        'website_info': website_info
        }
    
    return render(request, 'posts/about.html', context)


def all_posts(request):
    all_posts = Post.objects.all()
    paginator = Paginator(all_posts, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'posts': posts,
    }
    
    return render(request, 'posts/all_posts.html', context)


def author_all_posts(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    all_posts = Post.objects.filter(author=profile.user)
    
    context={
        'all_posts':all_posts,
        'profile': profile,
    }
    
    return render(request, 'posts/author_all_posts.html', context)