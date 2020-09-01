from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from account.api.serializers import UserSerializer

from account.api.serializers import RegisterSerializer

from account.api.permissons import NotAuthenticated

from account.api.throttles import RegisterThrottle


class ProfileView(RetrieveUpdateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class CreateUserView(CreateAPIView):
    throttle_classes = [RegisterThrottle]
    model = User.objects.all()
    serializer_class = RegisterSerializer
    # permission_classes = [NotAuthenticated]
