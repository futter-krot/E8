import threading
import time
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from nsqr.forms import AddPostForm
from nsqr.models import Result, Task
from .tasks import findpy
from celery.result import AsyncResult
# Create your views here.


class Threading(threading.Thread):
    def __init__(self, postdate, let, ids, task):
        self.postdate = postdate
        self.let = let
        self.ids = ids
        self.task = task
        self.status = findpy.AsyncResult(self.ids)
        threading.Thread.__init__(self)

    def run(self):
        Task.objects.filter(id=self.task).update(task_status=2)
        time.sleep(self.postdate)
        Task.objects.filter(id=self.task).update(task_status=3)
        self.let.update(status=self.status.status)
        print(self.status)


class ResultView(ListView):
    model = Result
    template_name = "nsqr/index.html"
    context_object_name = "results"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        context['nbar'] = 'home'
        return context


class TaskCreate(CreateView):
    model = Task
    template_name = "nsqr/add.html"
    form_class = AddPostForm
    success_url = reverse_lazy("nsqr:result-view")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nbar'] = 'hole'
        return context


def contact(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            task = form.save()
            x = findpy.delay(address)
            count = findpy(address)
            result = Result(
                address=address,
                words_count=count,
                http_status=200,
                task=task,
                status='STARTED'
            )
            result.save()
            let = Result.objects.filter(id=result.id)
            Threading(10, let, x.task_id, task.id).start()
        else:
            form = AddPostForm(prefix='tasks')
        return redirect('nsqr:result-view')
