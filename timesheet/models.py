from django.db import models
from django.contrib.auth.models import User
import datetime

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class Timesheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    break_time = models.IntegerField(default=60)  # Em minutos

    def __str__(self):
        return f"{self.user.username} - {self.project.name} - {self.start_time}"

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
