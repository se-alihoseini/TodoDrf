from django.urls import path
from rest_framework import routers
from . import views

app_name = 'task'
urlpatterns = [
    path('old/', views.OldTask.as_view(), name='old_task'),
]

router = routers.SimpleRouter()
router.register('todo', views.TodoViewSet, basename='my_model')
urlpatterns += router.urls
