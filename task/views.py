from builtins import filter

from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework import parsers
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from permissions import IsOwnerOrReadOnly
from .models import Todo, ImageTodo
from .serializer import TodoSerializer, ImageTodoSerializer
from django.shortcuts import get_object_or_404
from datetime import datetime


class TodoViewSet(viewsets.ViewSet):
    permission_classes = [IsOwnerOrReadOnly, ]
    parser_classes = [parsers.MultiPartParser]
    query_set = Todo.objects.all()

    def list(self, request):
        user = request.user
        query_set = self.query_set.filter(user=user, is_active=True)
        srz_data = TodoSerializer(instance=query_set, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)

    def create(self, request):
        srz_data = TodoSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.validated_data['user'] = request.user
            srz_data.save()
            return Response(data=srz_data.data, status=status.HTTP_201_CREATED)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        user = request.user
        query_set = self.query_set.filter(pk=pk, user=user, is_active=True)
        images = ImageTodo.objects.filter(todo_id__in=query_set)
        srz_data = TodoSerializer(instance=query_set, many=True)
        srz_img_data = ImageTodoSerializer(instance=images, many=True)
        data = [srz_data.data, srz_img_data.data]
        return Response(data=data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
        query_set = self.query_set.filter(pk=pk).first()
        srz_data = TodoSerializer(instance=query_set, data=request.POST, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        todo = self.query_set.filter(pk=pk).first()
        todo.is_active = False
        todo.save()
        return Response({'message': 'task deleted'})


class OldTask(generics.ListAPIView):
    serializer_class = TodoSerializer
    today = datetime.today()
    permission_classes = [IsOwnerOrReadOnly, ]
    queryset = Todo.objects.filter(date__lt=today)
    serializer_class = TodoSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ['is_active']
    search_fields = ('name',)

    def get(self, request, *args, **kwargs):
        user = request.user
        self.queryset = self.queryset.filter(user=user)
        sdate_search_query = request.GET.get('sdate_search')
        edate_search_query = request.GET.get('edate_search')
        if sdate_search_query != '' and sdate_search_query is not None:
            self.queryset = self.queryset.filter(date__gte=sdate_search_query)
        if edate_search_query != '' and edate_search_query is not None:
            self.queryset = self.queryset.filter(date__lte=edate_search_query)

        return self.list(request, *args, **kwargs)
