from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from person.models import Actor, Author
from person.serializers import (
    ActorDetailSerializer,
    ActorSerializer,
    AuthorSerializer,
)


class AuthorListCreateView(generics.ListCreateAPIView):
    serializer_class = AuthorSerializer

    def get(self, request):
        authors = Author.objects.all()
        serializer_class = AuthorSerializer(authors, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer_class = AuthorSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        return Response(
            serializer_class.errors, status=status.HTTP_400_BAD_REQUEST
        )


class ActorListCreateView(generics.ListCreateAPIView):
    serializer_class = ActorSerializer

    def get(self, request):
        actors = Actor.objects.all()
        serializer_class = ActorSerializer(actors, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer_class = ActorSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(
                serializer_class.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer_class.errors, status=status.HTTP_400_BAD_REQUEST
        )


class ActorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActorDetailSerializer

    def get(self, request, actor_id: int = None):
        actor_detail = Actor.objects.get(id=actor_id)
        serializer_class = ActorDetailSerializer(actor_detail, many=False)
        return Response(serializer_class.data, status=status.HTTP_200_OK)
