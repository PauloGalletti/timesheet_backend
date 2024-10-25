from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from timesheet.views import CustomAuthToken  # Importa a view customizada para o login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('timesheet.urls')),  # Incluindo URLs do app timesheet
    path('api/auth/login/', CustomAuthToken.as_view(), name='api_token_auth'),  # Endpoint de login para obter o token de autenticação
]
