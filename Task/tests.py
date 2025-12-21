from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Tasks
from .serializers import TaskSerializer
from rest_framework.test import APITestCase
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            email="test@example.com",
            password="pass123"
        )
        self.task = Tasks.objects.create(
            title="Test Task",
            description="Testing",
            user=self.user,
            status="pending",
            due_date=timezone.now() + timedelta(days=1)
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.status, "pending")
        self.assertEqual(self.task.user, self.user)


class TaskSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            email="test@example.com",
            password="pass123"
        )
        self.task = Tasks.objects.create(
            title="Test",
            user=self.user,
            due_date=timezone.now() + timedelta(days=1)
        )

    def test_valid_serializer(self):
        serializer = TaskSerializer(instance=self.task)
        self.assertEqual(serializer.data["title"], "Test")


class TaskAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            email="test@example.com",
            password="pass123"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_task(self):
        response = self.client.post(
            "/api/tasks/",
            {
                "title": "New Task",
                "description": "Testing task creation",
                "due_date": (timezone.now() + timedelta(days=1)).isoformat(),
                "status": "pending"
            },
            format="json"
        )
        print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "New Task")

    def test_list_tasks(self):
        Tasks.objects.create(
            title="Task 1",
            user=self.user,
            due_date=timezone.now() + timedelta(days=1)
        )
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
