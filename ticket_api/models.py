from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(max_length=200, unique=True)
    email = models.TextField()
    # add additional fields in here

    def __str__(self):
        return self.username


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


# class User(models.Model):
#     name = models.CharField(max_length=200)
#     email = models.TextField()
#     created_date = models.DateTimeField(default=timezone.now)
#     role = models.ForeignKey(Role, on_delete=models.CASCADE, default=None)
#     password = models.CharField(max_length=50, default='')
#     def publish(self):
#         self.save()
#     def __str__(self):
#         return self.name



class Issue(models.Model):
    type =  models.ForeignKey(IssueType, on_delete=models.CASCADE, default=None)    
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.ForeignKey(IssueStatus, on_delete=models.CASCADE, default=None)
    estimated_time = models.IntegerField()
    reporter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reporter', default=None)
    assignee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assignee', default=None)
    def __str__(self):
        return self.title
    def get_key_value(self, name):
        return getattr(self, name)


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='creator', default=None)


class ProjectIssueMap(models.Model):
    project =  models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project', default=None)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='issue', default=None)


class EventLog(models.Model):
    issue_id =  models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='issue_id', default=None)
    updated_field = models.CharField(max_length=20)
    previous_value = models.TextField()
    new_value = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)  

class Comment(models.Model):
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comment_issue_id', default=None)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author', default=None)
    text = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)

class Watcher(models.Model):
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='watcher_issue_id', default=None)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='watcher_user_id', default=None)
    
