from django.db import models


# Create your models here.

STATUS = (
    ("In Progress", "In Progress"),
    ("Completed", "Completed"),
)


class Task(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=25, choices=STATUS, default=STATUS[0][0])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.name
