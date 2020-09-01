from django.urls import path

from favourite.api.views import FavouriteListCreateView, FavouriteAPIView

app_name = 'favourite'

urlpatterns = [
    path('list-create', FavouriteListCreateView.as_view(), name='list-create'),
    path('update-delete/<pk>', FavouriteAPIView.as_view(), name='update-delete')
]
