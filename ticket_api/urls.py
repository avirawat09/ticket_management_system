from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path("issues", views.issue_list, name = 'issue_list'), 
    path("issues/<int:issue_id>", views.issue_single_update),     
    path("issues/<issue_parameter>/<issue_value>", views.issue_fetch_by_parameter), 
    
    path("project", views.project_list, name = 'project_list'),
    path("project/<int:project_id>", views.project_single_update, name = 'project_single_update'), 
    path("project/issue/<int:project_id>", views.project_issue_add, name = 'project_list'), 
    path("project/<project_parameter>/<parameter_value>", views.project_fetch_by_parameter, name = 'project_list'),
    
    

]