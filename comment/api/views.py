from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin

from .pagination import CommentPagination
from .permissons import IsOwner
from ..models import Comment
from ..api.serializers import CommentCreateSerializer, CommentListSerializer, CommentDeleteUpdateSerializer


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        """
        create
        """
        serializer.save(user=self.request.user)


class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    pagination_class = CommentPagination

    def get_queryset(self):
        queryset = Comment.objects.filter(parent=None)
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(post=query)
        return queryset


class CommentDeleteAPIView(DestroyAPIView, UpdateModelMixin, RetrieveModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteUpdateSerializer
    lookup_field = 'pk'
    permission_classes = [IsOwner]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CommentUpdateAPIView(UpdateAPIView, RetrieveModelMixin, DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteUpdateSerializer
    lookup_field = 'pk'
    permission_classes = [IsOwner]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
