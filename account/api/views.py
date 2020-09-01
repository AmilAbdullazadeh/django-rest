from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView, \
    RetrieveUpdateDestroyAPIView
from ..models import Post
from ..api.pagination import PostPagination
from ..api.serializers import PostSerializer, PostUpdateCreateSerializer
from rest_framework import filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated
)

from ..api.permissons import IsOwner


class PostListAPIView(ListAPIView, CreateModelMixin):
    serializer_class = PostSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    pagination_class = PostPagination

    def get_queryset(self):
        queryset = Post.objects.filter(draft=False)
        return queryset

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwner]


class PostUpdateAPIView(RetrieveUpdateDestroyAPIView, DestroyModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostUpdateCreateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwner]

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PostCreateAPIView(CreateAPIView, ListModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostUpdateCreateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
