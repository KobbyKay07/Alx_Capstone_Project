from django.urls import path
from .views import (TaskListCreateView, TaskDetailView, UserListCreateView, UserSignUpView, 
                    UserDetailView, mark_task_in_progress, mark_task_pending, mark_task_complete,
                    CategoryListCreateView, TaskHistoryListView, add_collaborator,
                    )
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

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
    path('tasks/<int:pk>/complete/', mark_task_complete, name='task-complete'),
     # Signup
    path("signup/", UserSignUpView.as_view(), name="user-signup"),
    # JWT login & refresh
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # JWT logout (blacklist refresh token)
    path("token/logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
    # Category endpoint
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    # History endpoint
    path("tasks/history/", TaskHistoryListView.as_view(), name="task-history"),
    # Collaborators endpoint
    path("tasks/<int:pk>/add-collaborator/", add_collaborator, name="add-collaborator")
]