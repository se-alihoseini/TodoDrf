from .models import Todo, ImageTodo
from rest_framework import serializers
from datetime import datetime


class ImageTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageTodo
        fields = "__all__"


class TodoSerializer(serializers.ModelSerializer):
    images = ImageTodoSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=True, use_url=False), write_only=True
    )

    class Meta:
        model = Todo
        fields = ('name', 'description', 'date', 'uploaded_images', 'images')

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        todo = Todo.objects.create(**validated_data)
        for image in uploaded_images:
            ImageTodo.objects.create(todo=todo, image=image)
        return todo

    def validate_date(self, value):
        now_date = datetime.now().date()
        if value < now_date:
            raise serializers.ValidationError('Date cannot be for the past')
        return value
