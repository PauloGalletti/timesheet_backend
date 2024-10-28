from django.urls import path
from .views import ProjectListCreateView, TimesheetListCreate, user_list_create, user_delete, ClientListCreateView

urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('timesheet/', TimesheetListCreate.as_view(), name='timesheet-list-create'),
    path('users/', user_list_create, name='user-list-create'),
    path('users/<str:username>/', user_delete, name='user-delete'),

    path('clients/', ClientListCreateView.as_view(), name='client-list-create'),
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
]
