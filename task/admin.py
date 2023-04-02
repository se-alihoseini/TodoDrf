from django.contrib import admin
from .models import Todo, ImageTodo


class ImageTodoAdmin(admin.TabularInline):
    model = ImageTodo


@admin.register(Todo)
class TodoRegister(admin.ModelAdmin):
    list_display = ('user', 'name', 'is_active')
    inlines = (ImageTodoAdmin,)

