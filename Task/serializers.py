from rest_framework import serializers
from .models import Tasks, Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id", "username", "email", "date_joined", "is_active"]

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = "__all__"