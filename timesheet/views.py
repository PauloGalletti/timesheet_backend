from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Project, Timesheet, Client
from .serializers import ProjectSerializer, TimesheetSerializer, ClientSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .models import Timesheet

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            "user_id": user.id, 
            'is_staff': user.is_staff,  # Retorna se o usuário é admin
        })
    
class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

# View para listar e criar Timesheets
class TimesheetListCreate(generics.ListCreateAPIView):
    queryset = Timesheet.objects.all()
    serializer_class = TimesheetSerializer
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem acessar

# View para listar e criar usuários - apenas para administradores
@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def user_list_create(request):
    if request.method == 'GET':
        users = User.objects.all()
        data = [{"username": user.username, "id": user.id, "is_staff": user.is_staff} for user in users]
        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        username = request.data.get("username")
        password = request.data.get("password")
        is_staff = request.data.get("is_staff", False)  # Define se o usuário é admin ou não

        if username and password:
            if User.objects.filter(username=username).exists():
                return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(username=username, password=password)
            user.is_staff = is_staff  # Define se o usuário será staff
            user.save()
            return Response({"username": user.username, "is_staff": user.is_staff}, status=status.HTTP_201_CREATED)

        return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

# View para excluir um usuário - apenas para administradores
@api_view(['DELETE'])
@permission_classes([IsAdminUser])  # Apenas administradores podem acessar
def user_delete(request, username):
    try:
        user = User.objects.get(username=username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def save_timesheet(request):
    user = request.user
    date = request.data.get('date')
    entrada = request.data.get('entrada')
    intervalo = request.data.get('intervalo')
    saida = request.data.get('saida')

    if user and date and entrada and intervalo and saida:
        timesheet = Timesheet.objects.create(
            user=user, date=date, entrada=entrada, intervalo=intervalo, saida=saida
        )
        return Response({"message": "Timesheet salvo com sucesso"}, status=status.HTTP_201_CREATED)
    return Response({"error": "Dados inválidos"}, status=status.HTTP_400_BAD_REQUEST)
