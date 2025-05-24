from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .models import News, Trivia, TriviaVote
from .serializers import NewsSerializer, TriviaSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes


class NewsListCreateView(ListCreateAPIView):
    queryset = News.objects.all().order_by('-published_at')
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class NewsDetailView(RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticatedOrReadOnly]


class TriviaViewSet(viewsets.ModelViewSet):
    queryset = Trivia.objects.all()
    serializer_class = TriviaSerializer



from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vote_trivia(request, pk):
    try:
        trivia = Trivia.objects.get(pk=pk)
    except Trivia.DoesNotExist:
        return Response({'detail': 'Trivia not found.'}, status=404)

    user = request.user
    vote_type = request.data.get('vote_type')

    if vote_type not in [TriviaVote.LIKE, TriviaVote.DISLIKE]:
        return Response({'detail': 'Invalid vote_type.'}, status=400)

    existing_vote = TriviaVote.objects.filter(user=user, trivia=trivia).first()

    if existing_vote:
        if existing_vote.vote_type == vote_type:
            # Agar foydalanuvchi xuddi shu ovozni yana bersa, ovozni bekor qilamiz (delete)
            existing_vote.delete()
            if vote_type == TriviaVote.LIKE:
                trivia.upvotes = max(trivia.upvotes - 1, 0)
            else:
                trivia.downvotes = max(trivia.downvotes - 1, 0)
            trivia.save()
            return Response({'detail': 'Ovoz bekor qilindi', 'upvotes': trivia.upvotes, 'downvotes': trivia.downvotes}, status=200)
        else:
            # Ovoz turini o'zgartiramiz (like -> dislike yoki dislike -> like)
            if existing_vote.vote_type == TriviaVote.LIKE:
                trivia.upvotes = max(trivia.upvotes - 1, 0)
                trivia.downvotes += 1
            else:
                trivia.downvotes = max(trivia.downvotes - 1, 0)
                trivia.upvotes += 1
            existing_vote.vote_type = vote_type
            existing_vote.save()
            trivia.save()
            return Response({'detail': 'Ovoz o\'zgartirildi', 'upvotes': trivia.upvotes, 'downvotes': trivia.downvotes}, status=200)
    else:

        TriviaVote.objects.create(user=user, trivia=trivia, vote_type=vote_type)
        if vote_type == TriviaVote.LIKE:
            trivia.upvotes += 1
        else:
            trivia.downvotes += 1
        trivia.save()
        return Response({'detail': 'Ovoz qo\'shildi', 'upvotes': trivia.upvotes, 'downvotes': trivia.downvotes}, status=201)




