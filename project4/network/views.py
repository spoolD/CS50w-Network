from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.core.paginator import Paginator
import json

from .models import User, Posting


def index(request):
    
    if request.path == '/following':
        # Make request to get all posts from people followed
        user = User.objects.get(username=request.user)
        postings = Posting.objects.filter(author__in=user.following.all()).order_by('-timestamp').annotate(Count('liked'))
    
    else:
        # Make request to get all posts sorted by descending timestamp and annotate number of likes
        postings = Posting.objects.all().order_by('-timestamp').annotate(Count('liked'))
        
    #Turn query into Paginator object
    paginator = Paginator(postings, 10)

    # Get page requested
    page_obj = paginator.get_page(request.GET.get('page', 1))
   
    return render(request, "network/index.html", {"postings": postings, "num_pages": range(1, paginator.num_pages + 1), "page_obj": page_obj})


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
    # New Post
    if request.method == 'POST':
        data = json.loads(request.body)
        post = Posting(
            author = request.user,
            body = data.get("content", ""),
        )
        post.save()
        return JsonResponse({"message": "Added post successfully."}, status=201)
    
    # Update Post
    else:
        data = json.loads(request.body)
        post = Posting.objects.get(pk=data["id"])
        post.body = data["body"]
        post.save()
        return JsonResponse({"message": "updated post successfully"}, status=201)

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

@csrf_exempt
@login_required
def like(request):
    user = User.objects.get(username=request.user)
    data = json.loads(request.body)
    post = Posting.objects.get(pk=data["id"])
    
    # User hasn't liked yet
    if request.user not in post.liked.all():
        post.liked.add(user)
        post.save()
        likes = post.liked.count()
        return JsonResponse({"message": "Liked successfully.", "likes": likes}, status=201)
    # User already liked
    else:
        likes = post.liked.count()
        return JsonResponse({"message": "User already liked.","likes": likes}, status=201)
    