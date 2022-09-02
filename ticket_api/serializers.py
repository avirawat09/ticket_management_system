from rest_framework import serializers 
from ticket_api.models import CustomUser, Issue, Project, ProjectIssueMap, EventLog, Comment, Watcher

class IssueSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Issue
        fields = ('id',
                  'type',
                  'title',
                  'description',
                  'status',
                  'estimated_time',
                  'reporter',
                  'assignee'
                )


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id',
                  'title',
                  'description',
                  'creator'
                )                 
        extra_kwargs = {'title': {'required': False}}

class ProjectIssueMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectIssueMap
        fields = ('id',
                  'project',
                  'issue'
                )                 


class EventLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLog
        fields = ('id',
                  'issue_id',
                  'updated_field',
                  'previous_value',
                  'new_value',
                  'timestamp'
                )                 


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id',
                  'issue_id',
                  'author',
                  'text',
                  'created_on',
                  'updated_on'
                )                 

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id',
#                   'name',
#                   'email',
#                   'password',
#                   'created_date',
#                   'role'
#                 )                 
#         extra_kwargs = {'name': {'required': False}}


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id',
                  'name',
                  'email',
                )                 
        extra_kwargs = {'name': {'required': False}}




class WatcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watcher
        fields = ('id',
                  'issue_id',
                  'user_id',
                )                 
        
