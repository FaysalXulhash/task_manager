from django.urls import path
from .views import TaskCreateView, TaskListView, TaskUpdateView,TaskDeleteView
from tasks import views
urlpatterns = [

    #path('create/', TaskCreateView.as_view(), name='task-create'),
    path('', TaskListView.as_view(), name='task-list'),
    #path('create/', views.createTask, name='task-create'),
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('update/<int:pk>/', TaskUpdateView.as_view(), name='update-task'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='delete-task'),
]
