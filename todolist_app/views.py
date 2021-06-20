from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import TaskList
from .forms import TaskForm
from  django.contrib import messages
from  django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            form.save(commit=False).manager = request.user
            form.save()
            messages.success(request,"New Task Added")
        return redirect('todolist')
    else:
        all_task = TaskList.objects.filter(manager = request.user)
        paginator = Paginator(all_task,1)
        page = request.GET.get("pg")
        all_tasks = paginator.get_page(page)

        return render(request, "todolist.html", {"all": all_task})

@login_required
def contact(request):
    return render(request, "contact.html", {})

@login_required
def about(request):
    return render(request, "about.html", {})

@login_required
def delete_task(request,task_id):
    task=TaskList.objects.get(pk = task_id)
    if task.manager == request.user:
        task.delete()
    return redirect('todolist')

@login_required
def edit_task(request,task_id):
    if request.method == "POST":
        task=TaskList.objects.get(pk = task_id)
        if task.manager == request.user:
            form = TaskForm(request.POST or None, instance=task)
            if form.is_valid():
                form.save()
                messages.success(request,"Task edited")
        return redirect('todolist')
    else:
        task_obj= TaskList.objects.get(pk=task_id)
        return render(request,'edit.html',{'task_obj':task_obj})

@login_required
def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.done = True
    task.save()

    return redirect('todolist')

@login_required
def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.done = False
    task.save()

    return redirect('todolist')