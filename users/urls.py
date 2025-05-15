from django.urls import path
from .views import UserListCreateView, UserDetailView, LoginView

app_name = 'users'

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
