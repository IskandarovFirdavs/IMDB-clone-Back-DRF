from django.db.models import Avg
from rest_framework import serializers
from .models import Genre, Title, Episode, Review, Watchlist, Rating


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name',)


class TitleSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def get_average_rating(self, obj):
        return obj.ratings.aggregate(avg=Avg('score'))['avg'] or 0

    def get_review_count(self, obj):
        return obj.reviews.count()


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = '__all__'


class EpisodeSerializer(serializers.ModelSerializer):
    title = serializers.StringRelatedField()
    parent_series = serializers.StringRelatedField()

    class Meta:
        model = Episode
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'created_at')


class WatchlistSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    title = serializers.StringRelatedField()

    class Meta:
        model = Watchlist
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    title = serializers.StringRelatedField()

    class Meta:
        model = Rating
        fields = '__all__'



from users.serializers import UserSerializer

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'