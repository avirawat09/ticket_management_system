from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Role, IssueStatus, IssueType, CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

admin.site.register(Role)
admin.site.register(IssueStatus)
admin.site.register(IssueType)

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username",]

admin.site.register(CustomUser, CustomUserAdmin)