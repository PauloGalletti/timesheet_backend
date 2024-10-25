from django.urls import path
from .views import ProjectListCreate, TimesheetListCreate, user_list_create, user_delete

urlpatterns = [
    path('projects/', ProjectListCreate.as_view(), name='project-list-create'),
    path('timesheet/', TimesheetListCreate.as_view(), name='timesheet-list-create'),
    path('users/', user_list_create, name='user-list-create'),
    path('users/<str:username>/', user_delete, name='user-delete'),
]
