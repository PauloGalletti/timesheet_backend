from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, Timesheet, Client, Profile

class TimesheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timesheet
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=Profile.role_choices, write_only=True)  # Campo write-only para o profile
    is_admin = serializers.BooleanField(default=False, write_only=True)  # Define como write-only

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'is_admin']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = validated_data.pop('role')
        is_admin = validated_data.pop('is_admin')
        
        # Cria o usuário com os dados restantes
        user = User.objects.create_user(**validated_data)
        user.is_staff = is_admin  # Define se o usuário é staff
        user.save()
        
        # Cria o perfil associado com `role` e `is_admin`
        Profile.objects.create(user=user, role=role, is_admin=is_admin)
        
        return user