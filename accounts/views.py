from django.shortcuts import redirect, render
from .forms import NewUserForm
from .models import Profile
from posts.models import Post
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# Create your views here.
def register_user(request):
    form = NewUserForm()
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            login(request, user)
            return redirect("/")
    
    context={'form': form}
    return render(request, 'accounts/registration.html', context)

@login_required
def profile(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'author.html', {'user': request.user, 'posts': posts})