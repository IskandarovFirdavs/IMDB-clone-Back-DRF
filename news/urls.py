from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    NewsListCreateView, NewsDetailView, TriviaViewSet, vote_trivia,
)

app_name = 'news'


router = DefaultRouter()
router.register(r'trivia', TriviaViewSet, basename='trivia')

urlpatterns = router.urls + [
    path('news/', NewsListCreateView.as_view(), name='news-list-create'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),
    path('trivia/<int:pk>/vote/', vote_trivia, name='vote_trivia'),

]
