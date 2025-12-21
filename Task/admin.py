from django.contrib import admin
from .models import Category, Tasks, TaskHistory

# Register your models here.

admin.site.register(Category)
admin.site.register(TaskHistory)
admin.site.register(Tasks)
