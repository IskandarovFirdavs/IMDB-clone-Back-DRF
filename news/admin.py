from django.contrib import admin

from news.models import News, TriviaVote, Trivia, Source


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_at', 'author', 'is_featured']
    list_filter = ['is_featured', 'published_at']
    search_fields = ['title', 'content']

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']
    search_fields = ['name']

@admin.register(Trivia)
class TriviaAdmin(admin.ModelAdmin):
    list_display = ['content', 'title', 'person', 'verified', 'upvotes']
    list_filter = ['verified', 'created_at']
    search_fields = ['content']

@admin.register(TriviaVote)
class TriviaVoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'trivia', 'vote_type']
    list_filter = ['vote_type']