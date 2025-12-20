from rest_framework import serializers
from .models import Tasks
from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "date_joined", "is_active"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = "__all__"
        read_only_fields = ["user","created_at", "updated_at", "completed_at"]

    def validate_due_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Due date must be in the future.")
        return value
    
    def validate_priority(self, value):
        valid_priorities = [choice[0] for choice in Tasks._meta.get_field('priority').choices]
        if value not in valid_priorities:
            raise serializers.ValidationError("Priority must be low, medium, or high.")
        return value
    
    def validate(self, data):
        if self.instance is None:
            if data.get("status") == "completed":
                raise serializers.ValidationError(
                    "New tasks cannot be created with status 'completed'."
                )
            return data
        
        new_status = data.get("status", self.instance.status)

        if self.instance.status == "completed" and new_status == "completed":
            editable_fields = set(data.keys()) - {"status"}
            if editable_fields:
                raise serializers.ValidationError(
                    "Completed tasks cannot be edited unless reverted to pending or in progress."
                )
            
        valid_transitions = {
            "pending": ["in_progress", "completed"],
            "in_progress": ["pending", "completed"],
            "completed": ["pending", "in_progress"],
        }

        current_status = self.instance.status
        if new_status not in valid_transitions.get(current_status, []):
            raise serializers.ValidationError(
                f"Invalid status transition from {current_status} to {new_status}."
            )
        
        return data
    
    def update(self, instance, validated_data):
        old_status = instance.status
        new_status = validated_data.get('status', old_status)

        if old_status != 'completed' and new_status == 'completed':
            instance.completed_at = timezone.now()
        elif old_status == 'completed' and new_status != 'completed':
            instance.completed_at = None
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance