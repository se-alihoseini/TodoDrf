from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date = models.DateField()
    description = models.CharField(max_length=400)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.name


class ImageTodo(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='image_todo', null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.todo.name
