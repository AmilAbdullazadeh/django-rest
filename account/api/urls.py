from django.urls import path

from account.views import ProfileView

from account.views import CreateUserView

app_name = 'account'

urlpatterns = [
    path('me', ProfileView.as_view(), name='me'),
    path('register', CreateUserView.as_view(), name='register'),
]
