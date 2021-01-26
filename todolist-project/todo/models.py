from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TodoList(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    timeCreated = models.DateTimeField(auto_now_add=True)
    importantFlag = models.BooleanField(default=False)
    completedFlag = models.BooleanField(default=False)
    dateCompleted = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #user = models.ForeignKey(User, on_delete = models.CASCADE, default=2)


    def __str__(self):
        return self.title
