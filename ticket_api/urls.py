from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path("issues", views.issue_list, name = 'issue_list'), 
    path("issues/<int:issue_id>", views.issue_detail_single), 
    path("project", views.project_list, name = 'project_list'), 
    path("project/issue/<int:project_id>", views.project_issue_add, name = 'project_list'), 
    
    

]