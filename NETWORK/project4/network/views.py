from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import User, Post, Follow
from .serializers import PostSerializer, FollowSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.pagination import PageNumberPagination


def index(request):
    return render(request, "network/index.html")


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


@api_view(["GET"])
def PostApi(request):
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10

        posts = Post.objects.order_by('-id')

        paging_post = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(paging_post, many=True)
        data = {
        'results': serializer.data,
        'count': paginator.page.paginator.count,
        'next': paginator.get_next_link(),
        'previous': paginator.get_previous_link()
        }
        return Response(data, status=status.HTTP_200_OK)


@api_view(["POST"])
@login_required
def posting(request):
    if request.method == 'POST':
        if request.POST.get('textData') or 'image' in request.FILES:
            text_data = request.POST.get('textData')
            if 'image' in request.FILES:
                uploaded_image = request.FILES['image']
            else:
                uploaded_image = ''
            temp = Post(post_image=uploaded_image, post_text=text_data, post_owner=request.user)
            temp.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def editPost(request, id):
    post = get_object_or_404(Post, id=id)
    text = request.POST.get('textData', '')
    image = request.FILES.get('image', None)

    print(text)
    if text or image:
        if image:
            post.post_image = image
        if text:
            post.post_text = text
        post.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@login_required
def PostDetailAPI(request, postId):
    post = get_object_or_404(Post, id=postId)
    if request.method == "GET":
        serializer = PostSerializer(post, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == "PUT":
        if request.user in post.post_like.all():
            post.post_like.remove(request.user)
            post.save()
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        else:
            post.post_like.add(request.user)
            post.save
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    if request.method == "DELETE":
        post.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET", "PUT"])
@login_required
def FollowApi(request, id):
    user = Follow.objects.get(account=User.objects.get(request.user))
    target_account = User.objects.get(id=id)
    account= Follow.objects.get(account=target_account)
    account_follower = account.follower.all()

    if request.method == "GET":
        serializer = FollowSerializer(account, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == "PUT":
        if request.user in account_follower:
            account_follower.remove(request.user)
            account.save()
            user.following.remove(target_account)
            user.save()
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        else:
            account_follower.add(request.user)
            account.save()
            user.following.add(target_account)
            user.save()
            serializer = FollowSerializer(account, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

@api_view(['GET'])
def check_like_status(request, post_id):
    user = request.user  # Get the current user

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({"message": "Post not found"}, status=404)

    liked = post.like_by_user(user)
    
    return Response({"liked": liked})


def profiles(request, id):
    return render(request, "network/profile.html", {'profile_id' : id})


@api_view(['GET'])
def profile(request, id):
    user = get_object_or_404(User, id=id)
    post = Post.objects.filter(post_owner=user).order_by('-id')
    if not post.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    follow = Follow.objects.get(account=user)
    followSerialize = FollowSerializer(follow, many=False)
    if post:
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paging_post = paginator.paginate_queryset(post, request)

        serializer = PostSerializer(paging_post, many=True)
        data = {
        'results': serializer.data,
        'follow': followSerialize.data,
        'count': paginator.page.paginator.count,
        'next': paginator.get_next_link(),
        'previous': paginator.get_previous_link()
        }
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)



def postUser(request, id):
    pass


def postFollowing(request,id):
    pass