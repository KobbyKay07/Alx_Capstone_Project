from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.http import HttpResponse
from rest_framework import generics
from .models import Users, Tasks
from .serializers import TaskSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

# Create your views here.
def home(request):
    return HttpResponse("Welcome to Task Management API")

def mark_task_pending(request,pk):
    try:
        task = Tasks.objects.get(pk=pk, user=request.user)
    except Tasks.DoesNotExist:
        return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

    task.is_completed = False
    task.completed_at = None
    task.status = 'pending'
    task.save()

    return Response(TaskSerializer(task).data)

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def mark_task_in_progress(request, pk):
    try:
        task = Tasks.objects.get(pk=pk, user=request.user)
    except Tasks.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    task.status = "in_progress"
    task.is_completed = False
    task.completed_at = None
    task.save()

    return Response(TaskSerializer(task).data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_task_completed(request,pk):
    try:
        task = Tasks.objects.get(pk=pk, user=request.user)
    except Tasks.DoesNotExist:
        return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

    task.is_completed = True
    task.completed_at = timezone.now()
    task.status = 'completed'
    task.save()

    return Response(TaskSerializer(task).data)

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
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['status', 'priority', 'due_date']
    ordering_fields = ['due_date', 'priority', 'created_at']
    search_fields = ['title', 'description']

    def get_queryset(self):  
        return Tasks.objects.filter(user=self.request.user)

# Retrieve, Update & Delete Task
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer    