from rest_framework.routers import DefaultRouter
from .views import (
    GenreViewSet, TitleViewSet, EpisodeViewSet,
    ReviewViewSet, WatchlistViewSet, RatingViewSet
)

router = DefaultRouter()
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
router.register(r'episodes', EpisodeViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'watchlists', WatchlistViewSet)
router.register(r'ratings', RatingViewSet)

urlpatterns = router.urls
