from unittest import result
from xml.dom.domreg import well_known_implementations
from django.utils import timezone
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.core import serializers
import json
from ticket_api.view_utils import insert_to_event_log, json_serialized, send_notification_to_watchers
from ticket_api.models import CustomUser, Issue, Project, ProjectIssueMap, Comment, Watcher
from ticket_api.serializers import IssueSerializer, ProjectSerializer, ProjectIssueMapSerializer, CommentSerializer, WatcherSerializer
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import permission_required


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class HelloView(APIView):
    permission_classes = (IsAuthenticated, )  
    def get(self, request):
        content = {'message': 'Hello, Authentication feature working fine'}
        return Response(content)

# Create your views here.
def user_list(request):
    return render(request, 'user/user_list.html', {})

# ISSUE VIEW
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
#@permission_required("", login_url='/signup/')
def issue_list(request):
    print(dir(request.user))
    print(request.user.get_all_permissions())
    if request.method == 'GET':
        issues = Issue.objects.all()
        users = CustomUser.objects.all()
        issue_serializer = IssueSerializer(issues, many=True)
        issue_serializer_data = issue_serializer.data
        for issue_data in issue_serializer_data:

            issue_data['reporter'] = users.filter(pk=issue_data['reporter']).values_list('username')[0][0]
            issue_data['assignee'] = users.filter(pk=issue_data['assignee']).values_list('username')[0][0]
            
        return JsonResponse(issue_serializer_data, safe=False)
    elif request.method =='POST':
        new_issue = JSONParser().parse(request)
        issue_serializer = IssueSerializer(data=new_issue)
        if issue_serializer.is_valid():
            issue_serializer.save()
            issue_id = issue_serializer.data['id']
            for key in ['reporter', 'assignee']:
                new_entry = {
                    "issue_id": issue_id,
                    "user_id": new_issue[key]
                    }
                watcher_serializer = WatcherSerializer(data = new_entry)
                if watcher_serializer.is_valid():
                    watcher_serializer.save()
            return JsonResponse(issue_serializer.data, status=status.HTTP_201_CREATED)    
        
        return JsonResponse(issue_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
#@permission_required("", login_url='/signup/')
def issue_single_update(request,issue_id):
    issues = Issue.objects.get(pk=issue_id)
    if request.method =='PUT':
        new_issue = JSONParser().parse(request)
        if 'reporter' in new_issue.keys():
            return JsonResponse({"details" : "issue reporter cannot be changed"}, status=status.HTTP_400_BAD_REQUEST)                
        issue_serializer = IssueSerializer(issues, data=new_issue)
        if issue_serializer.is_valid():
            issue_serializer.save()
            insert_to_event_log(issue_id, issues, new_issue)
            if len(set(new_issue.keys()).intersection({'title', 'assignee','description'}))>0:
                send_notification_to_watchers(issue_serializer.data)
        
            return JsonResponse(issue_serializer.data, status=status.HTTP_201_CREATED)    
        
        return JsonResponse(issue_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method =='DELETE':
        issues.delete()
        return JsonResponse({"details":"Sucessfully deleted"}, status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
#@permission_required("", login_url='/signup/')
def issue_fetch_by_parameter(request,issue_parameter, parameter_value):
    print('debuggg')
    if issue_parameter == 'id':
        issues = Issue.objects.get(pk=int(parameter_value))
        issue_serializer = IssueSerializer(issues)
        return JsonResponse(issue_serializer.data, safe=False)
    elif issue_parameter == 'title':
        issues = Issue.objects.filter(title=parameter_value).values()[0]
        issue_serializer = IssueSerializer(issues)
        return JsonResponse(issue_serializer.data, safe=False)

    elif issue_parameter == 'description':
        issues = Issue.objects.filter(description=parameter_value).values()[0]
        issue_serializer = IssueSerializer(issues)
        return JsonResponse(issue_serializer.data, safe=False)

    else:
        return JsonResponse({'detail': 'Wrong parameter'}, safe=False)
    


# PROJECT VIEW
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
#@permission_required("", login_url='/signup/')
def project_list(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        projects_serialized = json_serialized(projects)
        for each_project in projects_serialized:
            issue_list = []
            project_id = each_project['pk']
            project_issue_list = list(ProjectIssueMap.objects.filter( project=project_id ).values_list('issue'))
            if len(project_issue_list)>0:
                project_issue_list  = [item[0] for item in project_issue_list]
                project_issue_detail_list = Issue.objects.filter(pk__in=project_issue_list)
                project_issue_detail_list = json_serialized(project_issue_detail_list)
                issue_list = [{'id': item['pk'], **item['fields']} for item in project_issue_detail_list]
            each_project['issue_list'] = issue_list    
        projects_serialized = [{'id': item['pk'], **item['fields'], 'issue_list': item['issue_list']} for item in projects_serialized]
        return JsonResponse(projects_serialized, safe=False)
    elif request.method =='POST': 
        new_project = JSONParser().parse(request)
        print(new_project)
        project_serializer = ProjectSerializer(data=new_project)
        print(project_serializer)
        if project_serializer.is_valid():
            print(project_serializer)
        
            project_serializer.save()
            return JsonResponse(project_serializer.data, status=status.HTTP_201_CREATED)    
        
        return JsonResponse(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
#@permission_required("", login_url='/signup/')
def project_single_update(request,project_id):
    projects = Project.objects.get(pk=project_id)
    if request.method =='PUT':
        new_project = JSONParser().parse(request)
        project_serializer = ProjectSerializer(projects, data=new_project)
        if project_serializer.is_valid():
            project_serializer.save()
            return JsonResponse(project_serializer.data, status=status.HTTP_201_CREATED)    
        
        return JsonResponse(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method =='DELETE':
        projects.delete()
        return JsonResponse({"details":"Sucessfully deleted"}, status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
#@permission_required("", login_url='/signup/')
def project_issue_add(request, project_id):
    if request.method =='POST': 
        new_issue = JSONParser().parse(request)
        print(new_issue)
        issue_serializer = IssueSerializer(data=new_issue)
        print(issue_serializer)
        if issue_serializer.is_valid():
            issue_serializer.save()
            new_issue_id = issue_serializer.data['id']
            project_issue_map_item = {
                "project" : project_id,
                "issue" : new_issue_id
                }
            project_issue_map_serializer = ProjectIssueMapSerializer(data = project_issue_map_item)
            if project_issue_map_serializer.is_valid():
                project_issue_map_serializer.save()        
                return JsonResponse(project_issue_map_serializer.data, status=status.HTTP_201_CREATED)    
            else:
                return JsonResponse(project_issue_map_serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

        return JsonResponse(issue_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
#@permission_required("", login_url='/signup/')
def project_fetch_by_parameter(request,project_parameter, parameter_value):
    if project_parameter == 'id':
        projects = Project.objects.filter(pk=int(parameter_value))
    elif project_parameter == 'name':
        projects = Project.objects.filter(title=parameter_value)        
    else:
        return JsonResponse({'detail': 'Wrong parameter'}, safe=False)
    projects_serialized = json_serialized(projects)
    for each_project in projects_serialized:
        issue_list = []
        project_id = each_project['pk']
        project_issue_list = list(ProjectIssueMap.objects.filter( project=project_id ).values_list('issue'))
        if len(project_issue_list)>0:
            project_issue_list  = [item[0] for item in project_issue_list]
            project_issue_detail_list = Issue.objects.filter(pk__in=project_issue_list)
            project_issue_detail_list = json_serialized(project_issue_detail_list)
            issue_list = [{'id': item['pk'], **item['fields']} for item in project_issue_detail_list]
        each_project['issue_list'] = issue_list    
    projects_serialized = [{'id': item['pk'], **item['fields'], 'issue_list': item['issue_list']} for item in projects_serialized]
    return JsonResponse(projects_serialized, safe=False)


# Comments
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
#@permission_required("", login_url='/signup/')
def comment_issue(request, issue_id):
    if request.method == 'GET':
        comments = Comment.objects.filter(issue_id = issue_id)
        comment_serializer = CommentSerializer(comments, many=True)
        return JsonResponse(comment_serializer.data, safe=False)
    elif request.method =='POST':
        new_comment = JSONParser().parse(request)
        new_comment["issue_id"] = issue_id
        comment_serializer = CommentSerializer(data=new_comment)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return JsonResponse(comment_serializer.data, status=status.HTTP_201_CREATED)    
        
        return JsonResponse(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
#@permission_required("", login_url='/signup/')
def comment_issue_udpate(request,comment_id):
    comments = Comment.objects.get(pk=comment_id)
    if request.method =='PUT':
        new_comment = JSONParser().parse(request)
        new_comment['updated_on'] = timezone.now()
        comment_serializer = CommentSerializer(comments, data=new_comment)
        if comment_serializer.is_valid():
            comment_serializer.save()
            print(comment_serializer)
            return JsonResponse(comment_serializer.data, status=status.HTTP_201_CREATED)    
        
        return JsonResponse(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method =='DELETE':
        comments.delete()
        return JsonResponse({"details":"Sucessfully deleted"}, status=status.HTTP_204_NO_CONTENT)


# WATCHER

@api_view(['GET'])
@permission_classes([IsAuthenticated])
#@permission_required("", login_url='/signup/')
def watcher_list(request, issue_id):
    if request.method == 'GET':
        watchers = Watcher.objects.filter(issue_id = issue_id).values_list('user_id')
        watchers_list = [watcher[0] for watcher in watchers]
        usernames = CustomUser.objects.filter(pk__in=watchers_list).values_list('username')
        usernames_list = [username[0] for username in usernames]
        return JsonResponse(usernames_list, safe=False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
#@permission_required("", login_url='/signup/')
def watcher_add(request, issue_id, watcher_id):
    if request.method == 'POST':
        new_entry = {
            "issue_id": issue_id,
            "user_id": watcher_id
        }
        watcher_serializer = WatcherSerializer(data = new_entry)
        if watcher_serializer.is_valid():
            watcher_serializer.save()
            return JsonResponse(watcher_serializer.data, safe=False)
        return JsonResponse(watcher_serializer.errors, safe=False)


# REPORT
@api_view(['GET'])
@permission_classes([IsAuthenticated])
#@permission_required("", login_url='/signup/')
def report_open_issues(request):
    if request.method == 'GET':
        open_issues = Issue.objects.order_by().filter(status = 1)
        unique_users = open_issues.values_list('assignee').distinct()
        unique_users = [user[0] for user in unique_users]
        print(unique_users)
        result = []
        for each_user in unique_users:
            each_user_issues = {}
            each_open_issue_list = open_issues.filter(assignee = each_user).values()
            each_user_details = CustomUser.objects.filter(pk=each_user).values_list('username', 'email')
            each_user_issues['username'] = each_user_details[0][0] 
            each_user_issues['email'] = each_user_details[0][1]
            each_user_issues['issues_list'] =  list(each_open_issue_list)            
            result.append(each_user_issues)
        return JsonResponse(result, safe=False)


        