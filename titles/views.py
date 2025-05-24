from rest_framework import generics, permissions, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Genre, Title, Episode, Review, Watchlist, Rating
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    GenreSerializer,
    TitleSerializer,
    TitleCreateUpdateSerializer,
    EpisodeSerializer,
    ReviewSerializer,
    WatchlistSerializer,
    RatingSerializer
)


# Genre Views
class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = permissions.IsAuthenticatedOrReadOnly,
    lookup_field = 'pk'


class GenreRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'


# Title Views
class TitleListView(generics.ListAPIView):
    queryset = Title.objects.prefetch_related('genres').all()
    serializer_class = TitleSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberPagination


class TitleCreateView(generics.CreateAPIView):
    queryset = Title.objects.all()
    serializer_class = TitleCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]


class TitleRetrieveView(generics.RetrieveAPIView):
    queryset = Title.objects.prefetch_related('genres').all()
    serializer_class = TitleSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'


class TitleUpdateView(generics.UpdateAPIView):
    queryset = Title.objects.all()
    serializer_class = TitleCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'


class TitleDestroyView(generics.DestroyAPIView):
    queryset = Title.objects.all()
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'


# Episode Views
class EpisodeListCreateView(generics.ListCreateAPIView):
    queryset = Episode.objects.select_related('title', 'parent_series').all()
    serializer_class = EpisodeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class EpisodeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Episode.objects.select_related('title', 'parent_series').all()
    serializer_class = EpisodeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'


# Review Views
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.select_related('user', 'title').all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.select_related('user', 'title').all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


# Watchlist Views
class WatchlistListCreateView(generics.ListCreateAPIView):
    serializer_class = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Watchlist.objects.select_related('user', 'title').filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class WatchlistRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return Watchlist.objects.select_related('user', 'title').filter(user=self.request.user)



# Rating Views
class RatingListCreateView(generics.ListCreateAPIView):
    queryset = Rating.objects.select_related('user', 'title').all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RatingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.select_related('user', 'title').all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            return Response(
                {"detail": "You can only edit your own ratings."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            return Response(
                {"detail": "You can only delete your own ratings."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecentReviewListView(generics.ListAPIView):
    queryset = Review.objects.select_related('user', 'title').order_by('-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]