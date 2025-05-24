from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    GenreListCreateView, GenreRetrieveUpdateDestroyView,
    TitleListView, TitleCreateView, TitleRetrieveView, TitleUpdateView, TitleDestroyView, GenreViewSet,
    RecentReviewListView, WatchlistListCreateView, WatchlistRetrieveUpdateDestroyView, WatchlistListView
)


router = DefaultRouter()
router.register(r'genres', GenreViewSet, 'genre')

urlpatterns = [
    # Genre URLs
    # path('genres/', GenreListCreateView.as_view(), name='genre-list'),
    # path('genres/<int:pk>/', GenreRetrieveUpdateDestroyView.as_view(), name='genre-detail'),

    # Title URLs
    path('titles/', TitleListView.as_view(), name='title-list'),
    path('titles/create/', TitleCreateView.as_view(), name='title-create'),
    path('titles/<int:pk>/', TitleRetrieveView.as_view(), name='title-detail'),
    path('titles/<int:pk>/update/', TitleUpdateView.as_view(), name='title-update'),
    path('titles/<int:pk>/delete/', TitleDestroyView.as_view(), name='title-delete'),
    path('reviews/', RecentReviewListView.as_view(), name='recent-reviews'),
    path('watchlists/', WatchlistListCreateView.as_view(), name='watchlist-create'),
    path('watchlists/list/', WatchlistListView.as_view(), name='watchlist-list'),
    path('watchlists/<int:pk>/', WatchlistRetrieveUpdateDestroyView.as_view(), name='watchlist-detail'),

]

urlpatterns += router.urls
