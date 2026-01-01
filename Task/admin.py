from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category, Tasks, TaskHistory, CustomUser, Notification

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'profile_picture')}),
    )

admin.site.register(Category)
admin.site.register(TaskHistory)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Notification)
admin.site.register(Tasks)
