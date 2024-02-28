from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Group, Message
from django.urls import reverse
from django.db import IntegrityError
from .serializers import GroupSerializer, MessageSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

# Create your views here.
def index(request):
    return render(request, "chat/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "chat/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "chat/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "chat/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "chat/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "chat/register.html")


#Create group + initial member
@csrf_exempt
@api_view(['POST'])
def create_group(request):
    if request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#add member
@api_view(['POST'])
def add_member(request, groupId, userId):
    group = get_object_or_404(Group, pk=groupId)
    user = get_object_or_404(User, pk=userId)
    group.group_member.add(user)
    group.update_newest_message_time()
    return Response(status=status.HTTP_200_OK)


#retreieve group(id)
@api_view(['GET'])
def retrieve_group(request):
    if request.method == 'GET':
        groups = Group.objects.filter(group_member=request.user)
        serializer = GroupSerializer(groups, many=True)
        content = {
            'retrieve_group' : serializer.data,
        }
        return Response(content, content_type='application/json')


#retrieve chat
@api_view(['GET'])
def retrieve_chat(request):
    if request.method == 'GET':
        message = Message.objects.all()
        serializer = MessageSerializer(message, many=True)
        content = {
            'retrieve_chat' : serializer.data,
        }
        return Response(content, content_type='application/json')


#send chat
def new_message(request, group_name):
    pass