from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from users.decorators import admin_required
from .forms import CreateTaskForm
from .models import Task


# Create your views here.
@admin_required
def admin_tasks_view(request):
    tasks = Task.objects.all()

    form = CreateTaskForm(request.POST or None)
    errors = None
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.info(request, "Task added successfully.")
        return redirect("tasks:admin_task_list")
    if form.errors:
        errors = form.errors

    context = {
        "tasks": tasks,
        "form": form,
        "errors": errors
    }
    template_name = "tasks/admin_index.html"
    return render(request, template_name, context)


@login_required
def tasks_view(request):
    tasks = Task.objects.filter(user=request.user.id)

    form = CreateTaskForm(request.POST or None)
    errors = None
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.info(request, "Task added successfully.")
        return redirect("tasks:task_list")
    if form.errors:
        errors = form.errors

    context = {
        "tasks": tasks,
        "form": form,
        "errors": errors
    }
    template_name = "tasks/user_tasks.html"
    return render(request, template_name, context)


@login_required
def task_edit_view(request, id=None):
    instance = get_object_or_404(Task, id=id)
    form = CreateTaskForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.info(request, "Task updated successfully.")
        return HttpResponseRedirect("/tasks/")
    template_name = "tasks/task_edit.html"
    context = {
        "form": form,
    }
    return render(request, template_name, context)


@login_required
def task_delete_view(request, id=None):
    instance = get_object_or_404(Task, id=id)
    instance.delete()
    messages.info(request, "Task deleted successfully.")
    return redirect("tasks:task_list")
