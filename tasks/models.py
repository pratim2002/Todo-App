from django.db import models
from users.models import User

# Create your models here.

STATUS = (
    ("To Do", "To Do"),
    ("In Progress", "In Progress"),
    ("Testing", "Testing"),
    ("Completed", "Completed"),
)


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=25, choices=STATUS, default=STATUS[0][0], blank=True)
    assign_to = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='assigned_user', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user"]

    def __str__(self):
        return self.name
