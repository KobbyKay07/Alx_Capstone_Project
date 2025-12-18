from rest_framework import serializers
from .models import Tasks, Users
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id", "username", "email", "date_joined", "is_active"]

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = "__all__"

    def validate_due_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Due date must be in the future.")
        return value
    
    def validate_priority(self, value):
        if value not in dict(Tasks.PRIORITY_CHOICES).keys():
            raise serializers.ValidationError("Priority must be low, medium, or high.")
        return value
    
    def validate(self, data):
        new_status = data.get("status", self.instance.status if self.instance else "pending")

        # Completed tasks cannot be edited unless reverted
        if self.instance and self.instance.status == "completed":
            if new_status == "completed":
                raise serializers.ValidationError(
                    "Completed tasks cannot be edited unless reverted to pending or in progress."
                )

    # Ensure valid transitions
        valid_transitions = {
            "pending": ["in_progress", "completed"],
            "in_progress": ["pending", "completed"],
            "completed": ["pending", "in_progress"],
        }

        if self.instance:
            current_status = self.instance.status
            if new_status not in valid_transitions[current_status]:
                raise serializers.ValidationError(
                    f"Invalid status transition from {current_status} to {new_status}."
                )
        return data