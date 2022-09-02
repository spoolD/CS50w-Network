from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
import json

from .models import User, Posting


def index(request):
    # Make request to get all posts sorted by descending timestamp 
    postings = Posting.objects.all().order_by('-timestamp')
    postings = Posting.objects.annotate(Count('liked'))
    return render(request, "network/index.html", {"postings": postings})


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

@csrf_exempt
@login_required
def post(request):
    data = json.loads(request.body)
    post = Posting(
         author = request.user,
         body = data.get("content", ""),
     )
    post.save()
    return JsonResponse({"message": "Added post successfully."}, status=201)


def profile(request, author):
    get_author = User.objects.get(username=author)
    following = get_author.following.count()
    followers = get_author.followers.count()
    posts = Posting.objects.filter(author=get_author).order_by('-timestamp')
    
    # Intializes variable so you can't follow/unfollow yourself
    if request.user == get_author.username:
        follow_button = False
    else: 
        follow_button = True

    # Determine whether the button should initially say follow or unfollow
    user = User.objects.get(username=request.user)
    try:
        check_follow = user.following.get(username=author)
    except:
        check_follow = None
        
    if check_follow:
        button_text = 'Unfollow'
    else:
         button_text = 'Follow'

    return render(request, "network/profile.html", {"author": get_author, "following": following, "followers": followers, "posts": posts, "follow_button": follow_button, "button_text": button_text})

@csrf_exempt
@login_required
def follow(request):
    # Get data from JSON request
    data = json.loads(request.body)
    current_user = User.objects.get(username=request.user)
    action = data.get("type", "")
    person = User.objects.get(username = data.get("person", ""))
    
    # Update database with request
    if action == 'Follow':
        current_user.following.add(person)
        return JsonResponse({"message": "Followed successfully."}, status=201)
    else:
        current_user.following.remove(person)
        return JsonResponse({"message": "Unfollowed successfully."}, status=201)