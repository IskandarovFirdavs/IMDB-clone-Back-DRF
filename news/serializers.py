from rest_framework import serializers
from .models import News, Trivia



class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'published_at', 'author', 'related_title', 'related_person']


class TriviaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trivia
        fields = ['id', 'content', 'title', 'person']
