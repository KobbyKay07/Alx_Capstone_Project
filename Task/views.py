from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, BasePermission, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.http import HttpResponse
from rest_framework import generics
from .models import Tasks, Category, TaskHistory, Notification
from .serializers import (
    TaskSerializer, UserSerializer, CategorySerializer, TaskHistorySerializer, 
    NotificationSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.contrib.auth import get_user_model
from rest_framework.throttling import UserRateThrottle

# Create your views here.
User = get_user_model()

def home(request):
    return HttpResponse("Welcome to Task Management API")

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_task_pending(request,pk):
    try:
        task = Tasks.objects.get(pk=pk, user=request.user)
    except Tasks.DoesNotExist:
        return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task, data={"status": "pending"}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def mark_task_in_progress(request, pk):
    try:
        task = Tasks.objects.get(pk=pk, user=request.user)
    except Tasks.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task, data={"status": "in_progress"}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_task_complete(request,pk):
    try:
        task = Tasks.objects.get(pk=pk, user=request.user)
    except Tasks.DoesNotExist:
        return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task, data={"status": "completed"}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_collaborator(request, pk):
    try:
        task = Tasks.objects.get(pk=pk, user=request.user)
    except Tasks.DoesNotExist:
        return Response({"error": "Task not found or not owned by you."}, status=404)

    collaborator_id = request.data.get("collaborator_id")
    try:
        collaborator = User.objects.get(pk=collaborator_id)
    except User.DoesNotExist:
        return Response({"error": "Collaborator not found."}, status=404)

    task.collaborators.add(collaborator)
    return Response({"message": f"{collaborator.username} added as collaborator."})


class UserSignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# Create & List Users
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff

# Retrieve, Update & Delete User
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    
class IsOwnerOrCollaborator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.user == request.user or
            request.user in obj.collaborators.all() or
            request.user.is_staff
        )

# Create & List Tasks 
class TaskListCreateView(generics.ListCreateAPIView):
    throttle_classes = [UserRateThrottle]
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['status', 'priority', 'due_date']
    ordering_fields = ['due_date', 'priority', 'created_at']
    search_fields = ['title', 'description']

    def get_queryset(self):  
        return Tasks.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Retrieve, Update & Delete Task
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrCollaborator]

    def perform_update(self, serializer):
        old_status = self.get_object().status
        instance = serializer.save()
        new_status = instance.status

        if old_status != new_status:
            TaskHistory.objects.create(
                task=instance,
                user=self.request.user,
                status=new_status
            )

class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskHistoryListView(generics.ListAPIView):
    serializer_class = TaskHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TaskHistory.objects.filter(user=self.request.user)
    
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    