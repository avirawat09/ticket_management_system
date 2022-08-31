from django.contrib import admin

# Register your models here.
from .models import User, Role, IssueStatus, IssueType

admin.site.register(User)
admin.site.register(Role)
admin.site.register(IssueStatus)
admin.site.register(IssueType)