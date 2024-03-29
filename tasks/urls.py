from django.urls import path, include
from .views import TaskCreateView, TaskListView, TaskUpdateView,TaskDeleteView,TaskDetailView, addPhoto, deletePhoto, TaskViewSet
from tasks import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [

    #path('create/', TaskCreateView.as_view(), name='task-create'),
    path('', TaskListView.as_view(), name='task-list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    #path('create/', views.createTask, name='task-create'),
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('update/<int:pk>/', TaskUpdateView.as_view(), name='update-task'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='delete-task'),
    path('photo/<int:pk>/', addPhoto, name='task-photo'),
    path('delete/photo/<int:pk>/', deletePhoto, name='task-photo-delete'),
    path('api/v1/', include(router.urls)),

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)