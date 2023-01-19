import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, Follow


def index(request):
    posts = Post.objects.order_by('-timestamp').all()

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, "network/index.html", {
        'posts': posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def new_post(request):

    if request.method == 'GET':
        return render(request, "network/new_post.html")

    if request.method == 'POST':
        # Create new post
        post = request.POST['post']

        new_post = Post(post=post, poster=request.user)
        new_post.save()

        return HttpResponseRedirect(reverse('index'))

def profile(request, username):
    user = User.objects.get(username=username)
    posts = user.posts.order_by('-timestamp').all()
    following_user = False

    if request.method == 'GET':
        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        
        # Get follower and followings for the requested user
        follower = Follow.objects.filter(follower=user)
        followed = Follow.objects.filter(followed=user)

        try:
            # Get objects where current user is the follower
            following_objs = request.user.follower.all()
            # Check if current user is following requested user
            for u in following_objs:
                if user == u.followed:
                    following_user = True
        except:
            pass

        return render(request, 'network/profile.html', {
            'username': user,
            'posts': posts,
            'follower': len(follower),
            'followed': len(followed),
            'following_user': following_user
        })

    if request.method == 'POST':

        # Get the value of the submited action (Follow or Unfollow)
        action = request.POST.get('action')
        if action == 'Follow':
            f = Follow(follower=request.user, followed=user)
            f.save()
        else:
            f = Follow.objects.get(follower=request.user, followed=user)
            f.delete()

        return HttpResponseRedirect(reverse('profile', kwargs=({'username': username})))

@login_required
def following(request):

    all_posts = []
    # Get objects where current user is the follower
    following_objs = request.user.follower.all()

    # Itarate the following_objs to get all the user's post that the current user follows
    for u in following_objs:
        posts = Post.objects.filter(poster=u.followed)
        all_posts.extend(posts)

    sorted_posts = sorted(all_posts, key=lambda x: x.timestamp, reverse=True) 

    paginator = Paginator(sorted_posts, 10)
    page = request.GET.get('page')
    sorted_posts = paginator.get_page(page)



    return render(request, 'network/following.html', {
        'posts': sorted_posts
    })

@csrf_exempt
@login_required
def edit_post(request, post_id):

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('post') is not None:
            post.post = data['post']

        if data.get('like') == 'like':
            likes = post.likes.all()
            if request.user in likes:
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)

        post.save()
        return JsonResponse(post.serialize(), status=200)

    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)
