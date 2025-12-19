from django.urls import path
from .views import (TaskListCreateView, TaskDetailView, UserListCreateView, 
                    UserDetailView, mark_task_in_progress, mark_task_pending, mark_task_complete)

urlpatterns = [
    # User endpoints
    path('users/', UserListCreateView.as_view(), name='user_list_create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    # Task endpoints
    path('tasks/', TaskListCreateView.as_view(), name='task_list_create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    # Task status transition endpoints
    path('tasks/<int:pk>/pending/', mark_task_pending, name='task-pending'),
    path('tasks/<int:pk>/in-progress/', mark_task_in_progress, name='task-in-progress'),
    path('tasks/<int:pk>/complete/', mark_task_complete, name='task-complete')
]
