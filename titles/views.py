from rest_framework import viewsets
from .models import Genre, Title, Episode, Review, Watchlist, Rating
from .serializers import (
    GenreSerializer, TitleSerializer, TitleCreateUpdateSerializer,
    EpisodeSerializer, ReviewSerializer, WatchlistSerializer, RatingSerializer
)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.prefetch_related('genres').all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TitleCreateUpdateSerializer
        return TitleSerializer


class EpisodeViewSet(viewsets.ModelViewSet):
    queryset = Episode.objects.select_related('title', 'parent_series').all()
    serializer_class = EpisodeSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('user', 'title').all()
    serializer_class = ReviewSerializer


class WatchlistViewSet(viewsets.ModelViewSet):
    queryset = Watchlist.objects.select_related('user', 'title').all()
    serializer_class = WatchlistSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.select_related('user', 'title').all()
    serializer_class = RatingSerializer
