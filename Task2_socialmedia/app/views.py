from django.contrib.auth.models import User
from .models import Post, Like, Comment, Follow
from django.shortcuts import render, redirect
from .models import Post

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


# Home Page
def home(request):

    if request.method == 'POST':

        content = request.POST.get('content')

        if content:

            Post.objects.create(
                user=request.user,
                content=content
            )

            return redirect('home')

    posts = Post.objects.all().order_by('-created_at')

    return render(request, 'home.html', {
        'posts': posts
    })


# Register
def register_view(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('home')

    else:

        form = UserCreationForm()

    return render(request, 'register.html', {
        'form': form
    })


# Login
def login_view(request):

    if request.method == 'POST':

        form = AuthenticationForm(data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect('home')

    else:

        form = AuthenticationForm()

    return render(request, 'login.html', {
        'form': form
    })


# Logout
def logout_view(request):

    logout(request)

    return redirect('login')

def like_post(request, post_id):

    post = Post.objects.get(id=post_id)

    already_liked = Like.objects.filter(
        post=post,
        user=request.user
    )

    if not already_liked:

        Like.objects.create(
            post=post,
            user=request.user
        )

    return redirect('home')

def add_comment(request, post_id):

    if not request.user.is_authenticated:
        return redirect('login')

    post = Post.objects.get(id=post_id)

    if request.method == 'POST':

        text = request.POST.get('text')

        if text:

            Comment.objects.create(
                post=post,
                user=request.user,
                text=text
            )

    return redirect('home')

def profile(request, user_id):

    profile_user = User.objects.get(id=user_id)

    posts = Post.objects.filter(user=profile_user)

    followers_count = Follow.objects.filter(
        following=profile_user
    ).count()

    following_count = Follow.objects.filter(
        follower=profile_user
    ).count()

    already_following = False

    if request.user.is_authenticated:

        already_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'already_following': already_following
    }

    return render(request, 'profile.html', context)

def follow_user(request, user_id):

    if not request.user.is_authenticated:
        return redirect('login')

    user_to_follow = User.objects.get(id=user_id)

    already_following = Follow.objects.filter(
        follower=request.user,
        following=user_to_follow
    )

    if not already_following.exists():

        Follow.objects.create(
            follower=request.user,
            following=user_to_follow
        )

    return redirect('profile', user_id=user_id)