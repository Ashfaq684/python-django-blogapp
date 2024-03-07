from django.shortcuts import get_object_or_404, redirect, render
from .forms import NewUserForm, EditProfileForm
from .models import Profile
from posts.models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count


# Create your views here.
def register_user(request):
    form = NewUserForm()
    profile = None
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            login(request, user)
            return redirect("/")
    
    context={'form': form, 'profile':profile}
    return render(request, 'accounts/registration.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            # Authentication failed
            error_message = 'Invalid username or password'
            return render(request, 'accounts/login.html', {'error_message': error_message})
    else:
        return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request, slug):
    posts = Post.objects.filter(author=request.user)
    top_posts = Post.objects.filter(author = request.user).order_by('-view_count')[0:2]
    recent_posts = Post.objects.filter(author = request.user).order_by('-last_updated')[0:2]
    top_authors = User.objects.annotate(number=Count('post')).order_by('-number')[0:2]

    
    context = {
        'user': request.user,
        'posts': posts,
        'top_posts': top_posts,
        'recent_posts': recent_posts,
        'top_authors':top_authors,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after successful update
    else:
        form = EditProfileForm(instance=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})


def author_page(request, slug):
    profile = Profile.objects.get(slug=slug)
    top_posts = Post.objects.filter(author = profile.user).order_by('-view_count')[0:2]
    recent_posts = Post.objects.filter(author = profile.user).order_by('-last_updated')[0:2]
    top_authors = User.objects.annotate(number=Count('post')).order_by('-number')[0:2]
    
    context = {
        'profile':profile, 
        'top_posts':top_posts, 
        'recent_posts':recent_posts, 
        'top_authors':top_authors,
    }
    return render(request, 'accounts/author.html', context)