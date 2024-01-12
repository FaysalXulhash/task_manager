from django.shortcuts import render, redirect
from .models import Task, Photo
from .forms import TaskForm, PhotoForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import F
from django.db.models import Q
# Create your views here.
def home(request):
    return render (request, 'tasks/base.html')

#list view
class TaskListView(ListView):
    model = Task
    template_name = 'tasks/taskdetail.html'
    context_object_name = 'tasks'
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['priorities'] = ['Low', 'Medium', 'High']
    #     return context

    def get_queryset(self):
        #queryset = Task.objects.all().order_by(F('priority').desc())
        query = self.request.GET.get('search')
        if query:
            object_list = self.model.objects.filter(title__icontains=query)
        else:
            object_list = self.model.objects.all()
        return object_list

        # date_created = self.request.GET.get('date_created')
        # if date_created:
        #     queryset = queryset.filter(
        #         date_created__date=date_created
        #     )

        # due_date = self.request.GET.get('due_date')
        # if due_date:
        #     queryset = queryset.filter(
        #         due_date__date=due_date
        #     )

        # priority = self.request.GET.get('priority')
        # if priority:
        #     queryset = queryset.filter(
        #         priority=priority
        #     )

        # is_complete = self.request.GET.get('is_complete')
        # if is_complete == '1':
        #     queryset = queryset.filter(is_complete=True)
        # elif is_complete == '0':
        #     queryset = queryset.filter(is_complete=False)

        # return queryset


#detail view
class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
#create view 
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasks/task_create.html'
    form_class = TaskForm
    success_url = reverse_lazy('task-list')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
#delete view
class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('task-list')
    def test_func(self):
        task = self.get_object()
        if self.request.user == task.user:
            return True
        return False
# updateview
class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    template_name = 'tasks/task_update.html'
    form_class = TaskForm
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    def test_func(self):
        task = self.get_object()
        if self.request.user == task.user:
            return True
        return False