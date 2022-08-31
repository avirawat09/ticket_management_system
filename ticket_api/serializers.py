from rest_framework import serializers 
from ticket_api.models import Issue

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