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
        fields = (
            'id',
            'title_type',
            'primary_title',
            'original_title',
            'is_adult',
            'start_year',
            'end_year',
            'runtime_minutes',
            'genres',
            'poster',
            'plot',
            'average_rating',
            'num_votes',
            'review_count',
        )

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
    user = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

    def get_user(self, obj):
        from users.serializers import UserSerializer  # Lazy import
        return UserSerializer(obj.user).data

class WatchlistSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    title = serializers.PrimaryKeyRelatedField(queryset=Title.objects.all())

    class Meta:
        model = Watchlist
        fields = ['id', 'title', 'user', 'added_at', 'status']

    def validate_status(self, value):
        valid_statuses = [choice[0] for choice in Watchlist.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Status must be one of {valid_statuses}")
        return value

class WatchlistGetSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    title = TitleSerializer(read_only=True)

    class Meta:
        model = Watchlist
        fields = ['id', 'title', 'user', 'added_at', 'status']

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    title = serializers.StringRelatedField()

    class Meta:
        model = Rating
        fields = '__all__'