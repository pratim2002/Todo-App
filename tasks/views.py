from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CreateTaskForm
from .models import Task


# Create your views here.

def task_list_view(request):
    tasks = Task.objects.all()

    form = CreateTaskForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect('')

    context = {
        'tasks': tasks,
        'form': form
    }
    template_name = 'index.html'
    return render(request, template_name, context)


def task_delete_view(request, id=None):
    instance = get_object_or_404(Task, id=id)
    instance.delete()
    return redirect('/')
