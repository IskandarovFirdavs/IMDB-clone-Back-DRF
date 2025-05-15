from rest_framework import serializers
from .models import Genre, Title, Episode, Review, Watchlist, Rating


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class TitleSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


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
    user = serializers.StringRelatedField()
    title = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = '__all__'


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
