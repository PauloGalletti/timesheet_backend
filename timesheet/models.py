from django.db import models
from django.contrib.auth.models import User
import datetime

class Client(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="projects", null=True, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class Timesheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    atendimento_choices = (
        ('Sustentação', 'Sustentação'),
        ('Projetos', 'Projetos'),
        ('Atividades Internas', 'Atividades Internas'),
    )
    atendimento = models.CharField(max_length=50, choices=atendimento_choices)
    detalhes = models.TextField(blank=True, null=True)
    obs = models.TextField(blank=True, null=True)
    date = models.DateField()
    entrada = models.TimeField()
    intervalo = models.TimeField()
    saida = models.TimeField()
    total_horas = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        entrada_datetime = datetime.datetime.combine(self.date, self.entrada)
        saida_datetime = datetime.datetime.combine(self.date, self.saida)
        intervalo_duration = datetime.timedelta(hours=self.intervalo.hour, minutes=self.intervalo.minute)
        total_duration = (saida_datetime - entrada_datetime) - intervalo_duration
        self.total_horas = total_duration.total_seconds() / 3600
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    projects = models.ManyToManyField(Project)

    def __str__(self):
        return self.user.username

class CalendarNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    note = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class Timesheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    entrada = models.TimeField(default="00:00") 
    intervalo = models.TimeField(default="00:00") 
    saida = models.TimeField(default="00:00") 

    def __str__(self):
        return f"{self.user.username} - {self.date}"
