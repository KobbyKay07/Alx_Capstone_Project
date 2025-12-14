from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import Users, Tasks
from .serializers import TaskSerializer, UserSerializer

# Create your views here.
def home(request):
    return HttpResponse("Welcome to Task Management API")

# Create & List Users
class UserListCreateView(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

# Retrieve, Update & Delete User
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

# Create & List Tasks 
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer

# Retrieve, Update & Delete Task
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer    