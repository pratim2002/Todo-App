from django.urls import path
from . import views

app_name = 'tasks'
urlpatterns = [
    path("", views.task_list_view, name="task_list"),
    path("<id>/task_edit/", views.task_edit_view, name="task_edit"),
    path("<id>/task_delete/", views.task_delete_view, name="task_delete"),
]
