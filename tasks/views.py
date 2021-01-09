from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CreateTaskForm
from .models import Task


# Create your views here.

@login_required
def task_list_view(request):
    tasks = Task.objects.all()

    form = CreateTaskForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect("/tasks/")

    context = {"tasks": tasks, "form": form}
    template_name = "tasks/index.html"
    return render(request, template_name, context)


@login_required
def task_edit_view(request, id=None):
    instance = get_object_or_404(Task, id=id)
    form = CreateTaskForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
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
    return redirect("tasks:task_list")
