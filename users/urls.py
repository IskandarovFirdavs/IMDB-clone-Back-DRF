from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserListCreateView,
    UserDetailView,
    LoginView,
    CurrentUserView,
    PersonListCreateView,
    PersonDetailView,
    PersonFilmographyView
)

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='custom_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', UserListCreateView.as_view(), name='users_users_list'),
    path('<int:pk>/', UserDetailView.as_view(), name='users_users_detail'),
    path('me/', CurrentUserView.as_view(), name='users_users_me'),
    path('persons/', PersonListCreateView.as_view(), name='person_list_create'),
    path('persons/<int:pk>/', PersonDetailView.as_view(), name='person_detail'),
    path('persons/<int:pk>/filmography/', PersonFilmographyView.as_view(), name='person_filmography'),
]