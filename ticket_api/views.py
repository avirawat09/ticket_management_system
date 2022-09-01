from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from ticket_api.models import Issue, Project, ProjectIssueMap
from ticket_api.serializers import IssueSerializer, ProjectSerializer, ProjectIssueMapSerializer
from rest_framework.decorators import api_view
# Create your views here.
def user_list(request):
    return render(request, 'user/user_list.html', {})

# ISSUE VIEW
@api_view(['GET', 'POST'])
def issue_list(request):
    if request.method == 'GET':
        issues = Issue.objects.all()
        issue_serializer = IssueSerializer(issues, many=True)
        return JsonResponse(issue_serializer.data, safe=False)
    elif request.method =='POST':
        new_issue = JSONParser().parse(request)
        issue_serializer = IssueSerializer(data=new_issue)
        if issue_serializer.is_valid():
            issue_serializer.save()
            return JsonResponse(issue_serializer.data, status=status.HTTP_201_CREATED)    
        
        return JsonResponse(issue_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def issue_single_update(request,issue_id):
    issues = Issue.objects.get(pk=issue_id)
    if request.method =='PUT':
        new_issue = JSONParser().parse(request)
        if 'reporter' in new_issue.keys():
            return JsonResponse({"details" : "issue reporter cannot be changed"}, status=status.HTTP_400_BAD_REQUEST)    
        issue_serializer = IssueSerializer(issues, data=new_issue)
        if issue_serializer.is_valid():
            issue_serializer.save()
            return JsonResponse(issue_serializer.data, status=status.HTTP_201_CREATED)    
        
        return JsonResponse(issue_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method =='DELETE':
        issues.delete()
        return JsonResponse({"details":"Sucessfully deleted"}, status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
def issue_fetch_by_parameter(request,issue_parameter, parameter_value):
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
def project_list(request):
    print('inside project list')
    if request.method == 'GET':
        projects = Project.objects.all()
        for each_project in projects:
            project_id = each_project.id
            print('project id ', project_id)
            filtered_project_issue_map = ProjectIssueMap.objects.filter( project=project_id )
            print(filtered_project_issue_map)
            filtered_project_issue_map_serializer = ProjectIssueMapSerializer(data=  filtered_project_issue_map, many=True)
            if filtered_project_issue_map_serializer.is_valid():
                each_project.issue_list = filtered_project_issue_map_serializer.data
            else:
                print('not valid')    
        project_serializer = ProjectSerializer(projects, many=True)


        print(project_serializer.data)
        return JsonResponse(project_serializer.data, safe=False)
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
def project_fetch_by_parameter(request,project_parameter, parameter_value):
    if project_parameter == 'id':
        projects = Project.objects.get(pk=int(parameter_value))
        project_serializer = ProjectSerializer(projects)
        return JsonResponse(project_serializer.data, safe=False)
    elif project_parameter == 'name':
        projects = Project.objects.filter(title=parameter_value).values()[0]
        project_serializer = ProjectSerializer(projects)
        return JsonResponse(project_serializer.data, safe=False)

    else:
        return JsonResponse({'detail': 'Wrong parameter'}, safe=False)





