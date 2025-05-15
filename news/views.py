from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from .models import News, Trivia
from .serializers import NewsSerializer, TriviaSerializer


class NewsListCreateView(ListCreateAPIView):
    queryset = News.objects.all().order_by('-published_at')
    serializer_class = NewsSerializer


class NewsDetailView(RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    lookup_field = 'pk'


class TriviaListCreateView(ListCreateAPIView):
    queryset = Trivia.objects.all()
    serializer_class = TriviaSerializer


class TriviaDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Trivia.objects.all()
    serializer_class = TriviaSerializer
    lookup_field = 'pk'
