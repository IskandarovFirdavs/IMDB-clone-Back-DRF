from django.urls import path
from .views import (
    NewsListCreateView, NewsDetailView,
    TriviaListCreateView, TriviaDetailView
)

app_name = 'news'

urlpatterns = [
    path('news/', NewsListCreateView.as_view(), name='news-list-create'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),
    path('trivia/', TriviaListCreateView.as_view(), name='trivia-list-create'),
    path('trivia/<int:pk>/', TriviaDetailView.as_view(), name='trivia-detail'),
]
