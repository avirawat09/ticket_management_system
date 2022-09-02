from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('hello/', views.HelloView.as_view(), name ='authentication_check'),
    
    path("issues", views.issue_list, name = 'issue_list'), 
    path("issues/<int:issue_id>", views.issue_single_update),     
    path("issues/<issue_parameter>/<parameter_value>", views.issue_fetch_by_parameter), 
    
    path("project", views.project_list, name = 'project_list'),
    path("project/<int:project_id>", views.project_single_update, name = 'project_single_update'), 
    path("project/issue/<int:project_id>", views.project_issue_add, name = 'project_issue_add'), 
    path("project/<project_parameter>/<parameter_value>", views.project_fetch_by_parameter, name = 'project_fetch_by_parameter'),

    path("comment/issue/<issue_id>", views.comment_issue, name = 'comment_issue'),
    path("comment/<comment_id>", views.comment_issue_udpate, name = 'comment_update'),
    
    path("signup/", views.SignUpView.as_view(), name="signup"),

    path("watcher/<issue_id>", views.watcher_list, name = 'watcher_list'),
    path("watcher/<issue_id>/<watcher_id>", views.watcher_add, name = 'watcher_add'),
    
]