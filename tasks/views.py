from django.shortcuts import get_object_or_404, render, redirect
from .models import Task, Photo
from .forms import TaskForm, PhotoForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import F
from django.db.models import Q
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from .serializers import TaskSerializer
# Create your views here.
def home(request):
    return render (request, 'tasks/base.html')

#----
class TaskListAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
#list view
        
class TaskListView(ListView):
    model = Task
    template_name = 'tasks/tasklist.html'
    context_object_name = 'tasks'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['priorities'] = ['Low', 'Medium', 'High']
        return context
    def get_queryset(self):
        queryset = Task.objects.all().order_by(F('priority').desc())
        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(Q(title__icontains=query))
        
        date_created = self.request.GET.get('date_created')
        if date_created:
            queryset = queryset.filter(
                date_created__date=date_created
            )

        due_date = self.request.GET.get('due_date')
        if due_date:
            queryset = queryset.filter(
                due_date__date=due_date
            )

        priority = self.request.GET.get('priority')
        if priority:
            queryset = queryset.filter(
                priority=priority
            )

        # is_complete = self.request.GET.get('is_complete')
        # if is_complete == '1':
        #     queryset = queryset.filter(is_complete=True)
        # elif is_complete == '0':
        #     queryset = queryset.filter(is_complete=False)

        return queryset


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

#add photo in task
def addPhoto(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.task = task
            photo.save()
            messages.success(request, 'Photo added successfully.')
            return redirect('task-detail', pk=task.pk)
    else:
        form = PhotoForm()
    return render(request, 'tasks/addphoto.html', {'form': form})

#delete photo
def deletePhoto(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    task_pk = photo.task.pk
    photo.delete()
    messages.success(request, 'Photo deleted successfully.')
    return redirect('task-detail', pk=task_pk)