# Task/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .models import Tasks, Notification

@receiver(post_save, sender=Tasks)
def task_due_soon_notification(sender, instance, created, **kwargs):
    """
    Trigger a notification if a task is due within 24 hours.
    Avoid duplicates by checking existing unread notifications.
    """
    if instance.due_date - timezone.now() <= timedelta(hours=24):
        already_exists = Notification.objects.filter(
            user=instance.user,
            task=instance,
            message__icontains="due soon",
            is_read=False
        ).exists()

        if not already_exists:
            Notification.objects.create(
                user=instance.user,
                task=instance,
                message=f"Task '{instance.title}' is due soon!"
            )