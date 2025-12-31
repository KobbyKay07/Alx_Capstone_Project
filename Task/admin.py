from django.contrib import admin
from .models import Category, Tasks, TaskHistory, CustomUser, Notification

# Register your models here.

admin.site.register(Category)
admin.site.register(TaskHistory)
admin.site.register(CustomUser)
admin.site.register(Notification)
admin.site.register(Tasks)
