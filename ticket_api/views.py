from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from ticket_api.models import Issue
from ticket_api.serializers import IssueSerializer
from rest_framework.decorators import api_view
# Create your views here.
def user_list(request):
    return render(request, 'user/user_list.html', {})


@api_view(['GET', 'POST', 'DELETE'])
def issue_list(request):
    if request.method == 'GET':
        issues = Issue.objects.all()
        print("LOG: issues ", issues)
        issue_serializer = IssueSerializer(issues, many=True)
        print("LOG: issuesserializer ", issue_serializer)

        return JsonResponse(issue_serializer.data, safe=False)

