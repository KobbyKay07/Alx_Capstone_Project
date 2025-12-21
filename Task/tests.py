from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Tasks
from .serializers import TaskSerializer

# Create your tests here.
User = get_user_model()

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="pass123")
        self.task = Tasks.objects.create(
            title="Test Task",
            description="Testing",
            user=self.user,
            status="pending"
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.status, "pending")
        self.assertEqual(self.task.user, self.user)

class TaskSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="pass123")
        self.task = Tasks.objects.create(title="Test", user=self.user)

    def test_valid_serializer(self):
        serializer = TaskSerializer(instance=self.task)
        self.assertEqual(serializer.data["title"], "Test")