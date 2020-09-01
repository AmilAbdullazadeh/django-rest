from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, \
    RetrieveUpdateDestroyAPIView

from favourite.api.serializers import FavouriteListCreateAPISerializer, FavouriteAPISerializer
from favourite.models import Favourite
from favourite.api.permissons import IsOwner

from favourite.api.pagination import FavouritePagination
from rest_framework.permissions import IsAuthenticated


class FavouriteListCreateView(ListCreateAPIView):
    serializer_class = FavouriteListCreateAPISerializer
    pagination_class = FavouritePagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavouriteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteAPISerializer
    lookup_field = 'pk'
    permission_classes = [IsOwner]
