from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Tasks, Category, TaskHistory, Notification
from .serializers import TaskSerializer
from rest_framework.test import APITestCase
from django.utils import timezone
from datetime import timedelta

User = get_user_model()
"""
Models & Serializers Tests
"""

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


class CategoryTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", email="test@example.com", password="pass123")
        self.category = Category.objects.create(name="Work", user=self.user)

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Work")
        self.assertEqual(self.category.user, self.user)


class TaskHistoryTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", email="test@example.com", password="pass123")
        self.task = Tasks.objects.create(
            title="History Task",
            description="Testing history",
            user=self.user,
            status="pending",
            due_date=timezone.now() + timedelta(days=1)
        )
        self.history = TaskHistory.objects.create(task=self.task, status="created", user=self.user)

    def test_history_entry(self):
        self.assertEqual(self.history.task, self.task)
        self.assertEqual(self.history.status, "created")
        self.assertEqual(self.history.user, self.user)


class RecurrenceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", email="test@example.com", password="pass123")
        self.task = Tasks.objects.create(
            title="Recurring Task",
            description="Daily task",
            user=self.user,
            status="pending",
            due_date=timezone.now() + timedelta(days=1),
            recurrence="daily"
        )

    def test_recurrence_field(self):
        self.assertEqual(self.task.recurrence, "daily")


class NotificationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", email="test@example.com", password="pass123")
        self.task = Tasks.objects.create(
            title="Notify Task",
            description="Testing notifications",
            user=self.user,
            status="pending",
            due_date=timezone.now() + timedelta(days=1)
        )
        self.notification = Notification.objects.create(task=self.task, user=self.user, message="Task due soon")

    def test_notification_creation(self):
        self.assertEqual(self.notification.task, self.task)
        self.assertEqual(self.notification.user, self.user)
        self.assertEqual(self.notification.message, "Task due soon")


class CollaboratorTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", email="owner@example.com", password="pass123")
        self.collaborator = User.objects.create_user(username="collab", email="collab@example.com", password="pass123")
        self.task = Tasks.objects.create(
            title="Collab Task",
            description="Testing collaborators",
            user=self.owner,
            status="pending",
            due_date=timezone.now() + timedelta(days=1)
        )
        self.task.collaborators.add(self.collaborator)

    def test_collaborator_added(self):
        self.assertIn(self.collaborator, self.task.collaborators.all())

"""
API Tests
"""
class CategoryAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", email="test@example.com", password="pass123")
        self.client.force_authenticate(user=self.user)

    def test_create_category(self):
        response = self.client.post("/api/categories/", {"name": "Work"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "Work")

    def test_list_categories(self):
        Category.objects.create(name="Personal", user=self.user)
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class CollaboratorAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", email="owner@example.com", password="pass123")
        self.collaborator = User.objects.create_user(username="collab", email="collab@example.com", password="pass123")
        self.client.force_authenticate(user=self.owner)
        self.task = Tasks.objects.create(
            title="Collab Task",
            description="Testing collaborators",
            user=self.owner,
            due_date=timezone.now() + timedelta(days=1)
        )

    def test_add_collaborator(self):
        response = self.client.post(f"/api/tasks/{self.task.id}/add-collaborator/", {"collaborator_id": self.collaborator.id}, format="json")
        self.assertEqual(response.status_code, 200)
    
    def test_list_collaborators(self):
        self.task.collaborators.add(self.collaborator)
        response = self.client.get(f"/api/tasks/{self.task.id}/collaborators/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class RecurrenceAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", email="test@example.com", password="pass123")
        self.client.force_authenticate(user=self.user)

    def test_create_recurring_task(self):
        response = self.client.post("/api/tasks/", {
            "title": "Daily Task",
            "description": "Recurring",
            "due_date": (timezone.now() + timedelta(days=1)).isoformat(),
            "status": "pending",
            "recurrence": "daily"
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["recurrence"], "daily")


class NotificationAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", email="test@example.com", password="pass123")
        self.client.force_authenticate(user=self.user)
        self.task = Tasks.objects.create(
            title="Notify Task",
            description="Testing notifications",
            user=self.user,
            due_date=timezone.now() + timedelta(days=1)
        )
        Notification.objects.create(task=self.task, user=self.user, message="Task due soon")

    def test_list_notifications(self):
        response = self.client.get("/api/notifications/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)


class HistoryAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", email="test@example.com", password="pass123")
        self.client.force_authenticate(user=self.user)
        self.task = Tasks.objects.create(
            title="History Task",
            description="Testing history",
            user=self.user,
            due_date=timezone.now() + timedelta(days=1)
        )
        TaskHistory.objects.create(task=self.task, status="created", user=self.user)

    def test_list_history(self):
        response = self.client.get("/api/tasks/history/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
