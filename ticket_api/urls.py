from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path("issues", views.issue_list,name = 'issue_list'),   
]