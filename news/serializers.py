from rest_framework import serializers
from .models import News, Trivia
from django.utils.timezone import now
from django.contrib.humanize.templatetags.humanize import naturaltime


class NewsSerializer(serializers.ModelSerializer):
    # Adding human-readable time
    time_since_published = serializers.SerializerMethodField()

    # Adding detailed related objects
    related_title_detail = serializers.SerializerMethodField()
    related_person_detail = serializers.SerializerMethodField()
    author_name = serializers.CharField(source='author.username', read_only=True)

    # Adding engagement metrics (if available)
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    # Adding featured image URL
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            'id', 'title', 'content', 'published_at', 'time_since_published',
            'author', 'author_name', 'related_title', 'related_title_detail',
            'related_person', 'related_person_detail', 'like_count',
            'comment_count', 'image_url', 'slug'  # Adding slug if your model has it
        ]
        read_only_fields = ['published_at', 'author']
        extra_kwargs = {
            'content': {'write_only': True}  # Or make it write_only for certain actions
        }

    def get_time_since_published(self, obj):
        return naturaltime(obj.published_at)

    def get_related_title_detail(self, obj):
        if obj.related_title:
            return {
                'id': obj.related_title.id,
                'name': obj.related_title.primary_title,
                'type': obj.related_title.title_type
            }
        return None

    def get_related_person_detail(self, obj):
        if obj.related_person:
            return {
                'id': obj.related_person.id,
                'name': obj.related_person.__str__() if hasattr(obj.related_person, '__str__') else str(
                    obj.related_person),
            }
        return None

    def get_like_count(self, obj):
        # If i have a likes system
        return getattr(obj, 'like_count', obj.likes.count() if hasattr(obj, 'likes') else 0)

    def get_comment_count(self, obj):
        # If i have comments
        return getattr(obj, 'comment_count', obj.comments.count() if hasattr(obj, 'comments') else 0)

    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return obj.image.url
        return None

    def validate(self, data):
        # Custom validation example
        if len(data.get('title', '')) < 10:
            raise serializers.ValidationError("Title must be at least 10 characters long.")
        return data


class TriviaSerializer(serializers.ModelSerializer):
    # Adding detailed relationships
    title_detail = serializers.SerializerMethodField()
    person_detail = serializers.SerializerMethodField()

    # Adding verification status
    is_verified = serializers.BooleanField(source='verified', read_only=True)

    # Adding popularity metrics
    upvotes = serializers.IntegerField(read_only=True)

    # Adding source information
    source_name = serializers.CharField(source='source.name', read_only=True)

    class Meta:
        model = Trivia
        fields = [
            'id', 'content', 'title', 'title_detail',
            'person', 'person_detail', 'is_verified',
            'upvotes', 'source', 'source_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_title_detail(self, obj):
        if obj.title:
            return {
                'id': obj.title.id,
                'name': obj.title.name,
                'year': obj.title.release_date.year
            }
        return None

    def get_person_detail(self, obj):
        if obj.person:
            return {
                'id': obj.person.id,
                'name': obj.person.name,
                'role': obj.person.main_role
            }
        return None

    def validate_content(self, value):
        if len(value) < 20:
            raise serializers.ValidationError("Trivia content must be at least 20 characters long.")
        return value


# Additional serializers for different contexts
class NewsListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing news
    """
    excerpt = serializers.SerializerMethodField()
    author_name = serializers.CharField(source='author.username')

    class Meta:
        model = News
        fields = ['id', 'title', 'excerpt', 'author_name', 'published_at', 'image_url']

    def get_excerpt(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content


class TriviaListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing trivia
    """
    content_preview = serializers.SerializerMethodField()

    class Meta:
        model = Trivia
        fields = ['id', 'content_preview', 'title', 'person', 'upvotes']

    def get_content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content