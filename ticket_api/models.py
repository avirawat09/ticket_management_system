from django.conf import settings
from django.db import models
from django.utils import timezone

# BUG, TASK, STORY, EPIC 
class IssueType(models.Model):
    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name

# OPEN, INPROGRESS, INREVIEW, CODECOMPLETE, DONE
class IssueStatus(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

# ADMIN, PROJECTMANAGER, STANDARD
class Role(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=None)
    def publish(self):
        self.save()
    def __str__(self):
        return self.name



class Issue(models.Model):
    type =  models.ForeignKey(IssueType, on_delete=models.CASCADE, default=None)    
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.ForeignKey(IssueStatus, on_delete=models.CASCADE, default=None)
    estimated_time = models.IntegerField()
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporter', default=None)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignee', default=None)
    def __str__(self):
        return self.title





