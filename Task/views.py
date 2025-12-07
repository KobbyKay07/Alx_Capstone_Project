from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import tasks
from .serializers import TaskSerializer

# Create your views here.
def home(request):
    return HttpResponse("Welcome to Task Management API")

# Create & List Tasks 
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = tasks.objects.all()
    serializer_class = TaskSerializer

# Retrieve, Update & Delete Task
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = tasks.objects.all()
    serializer_class = TaskSerializer    