from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from movie.models import Movie
from person.models import Actor, Author
from person.serializers import (
    ActorDetailSerializer,
    ActorSerializer,
    AuthorDetailSerializer,
    AuthorSerializer,
    AuthorStatisticSerializer,
)


class AuthorListCreateView(generics.ListCreateAPIView):
    serializer_class = AuthorSerializer

    def get(self, request: dict) -> Response:
        authors = Author.objects.all()
        serializer_class = AuthorSerializer(authors, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def post(self, request: dict) -> Response:
        serializer_class = AuthorSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        return Response(
            serializer_class.errors, status=status.HTTP_400_BAD_REQUEST
        )


class AuthorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AuthorDetailSerializer

    def get(self, request: dict, author_id: int = None) -> Response:
        author_detail = Author.objects.get(id=author_id)
        serializer_class = AuthorDetailSerializer(author_detail, many=False)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def patch(self, request: dict, author_id: int = None) -> Response:
        try:
            name = request.data["name"]
            genre = request.data["genre"]
            birth_date = request.data["birth_date"]
            nationality = request.data["nationality"]
        except AssertionError as e:
            return Response(
                f"An error occured {e}!", status=status.HTTP_400_BAD_REQUEST
            )
        try:
            author_detail = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return Response(
                f"Author does not exist!", status=status.HTTP_400_BAD_REQUEST
            )
        serializer_class = AuthorDetailSerializer(
            author_detail, data=request.data, partial=False
        )
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(
                serializer_class.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer_class.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request: dict, author_id: int = None) -> Response:
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return Response(
                f"Author does not exist!", status=status.HTTP_400_BAD_REQUEST
            )
        try:
            author.delete()
            return Response(
                f"Author has been deleted successfully!",
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                f"An error occured {e}!", status=status.HTTP_400_BAD_REQUEST
            )


class ActorListCreateView(generics.ListCreateAPIView):
    serializer_class = ActorSerializer

    def get(self, request: dict) -> Response:
        actors = Actor.objects.all()
        serializer_class = ActorSerializer(actors, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def post(self, request: dict) -> Response:
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

    def get(self, request: dict, actor_id: int = None) -> Response:
        actor_detail = Actor.objects.get(id=actor_id)
        serializer_class = ActorDetailSerializer(actor_detail, many=False)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def patch(self, request: dict, actor_id: int = None) -> Response:
        try:
            name = request.data["name"]
            genre = request.data["genre"]
            birth_date = request.data["birth_date"]
            nationality = request.data["nationality"]
        except AssertionError as e:
            return Response(
                f"An error occured {e}!", status=status.HTTP_400_BAD_REQUEST
            )
        try:
            actor_detail = Actor.objects.get(id=actor_id)
        except Actor.DoesNotExist:
            return Response(
                f"Actor does not exist!", status=status.HTTP_400_BAD_REQUEST
            )
        serializer_class = ActorDetailSerializer(
            actor_detail, data=request.data, partial=False
        )
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(
                serializer_class.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer_class.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request: dict, actor_id: int = None) -> Response:
        try:
            actor_detail = Actor.objects.get(id=actor_id)
        except Actor.DoesNotExist:
            return Response(
                f"Actor does not exist!", status=status.HTTP_400_BAD_REQUEST
            )
        try:
            actor_detail.delete()
            return Response(
                f"Actor has been deleted successfully!",
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                f"An error occured {e}!", status=status.HTTP_400_BAD_REQUEST
            )


class AuthorStatisticView(generics.RetrieveAPIView):
    serializer_class = AuthorStatisticSerializer

    def get(self, request: dict) -> Response:
        movies = Movie.objects.all()
        serializer_class = AuthorStatisticSerializer(movies, many=False)
        return Response(serializer_class.data, status=status.HTTP_200_OK)
