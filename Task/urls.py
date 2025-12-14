from django.urls import path
from .views import TaskListCreateView, TaskDetailView, UserListCreateView, UserDetailView

urlpatterns = [
    # User endpoints
    path('users/', UserListCreateView.as_view(), name='user_list_create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    # Task endpoints
    path('tasks/', TaskListCreateView.as_view(), name='task_list_create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
]