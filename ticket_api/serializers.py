from rest_framework import serializers 
from ticket_api.models import Issue, Project, ProjectIssueMap

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

