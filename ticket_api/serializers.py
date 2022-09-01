from rest_framework import serializers 
from ticket_api.models import Issue, Project, ProjectIssueMap, EventLog, Comment

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

