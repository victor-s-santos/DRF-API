from django.db.models import Q

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from movie.models import Category, Movie
from movie.serializers import (
    CategorySerializer,
    MovieDetailSerializer,
    MovieSerializer,
)


class MovieListCreateView(generics.ListCreateAPIView):
    serializer_class = MovieSerializer

    def get(self, request) -> Response:
        movie_filters = self.movie_filters(request)
        person_filters = self.person_filters(request)
        filters = Q()
        if movie_filters:
            filters &= movie_filters
        if person_filters:
            filters &= person_filters
        elif not movie_filters and not person_filters:
            movies = Movie.objects.all()
            serializer_class = MovieSerializer(movies, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        movies = Movie.objects.filter(filters)
        serializer_class = MovieSerializer(movies, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def movie_filters(self, request) -> Q:
        title = request.query_params.get("title", None)
        category = request.query_params.get("category", None)
        publication_date = request.query_params.get("publication_date", None)

        if not (
            (title is not None)
            or (category is not None)
            or (publication_date is not None)
        ):
            return False
        filters = Q()
        if title:
            filters &= Q(title=title)
        if category:
            filters &= Q(category=category)
        if publication_date:
            filters &= Q(publication_date=publication_date)
        return filters

    def person_filters(self, request) -> Q:
        actor_name = request.query_params.get("actor_name", None)
        author_name = request.query_params.get("author_name", None)
        if not ((actor_name is not None) or (author_name is not None)):
            return False
        filters = Q()
        if actor_name:
            filters &= Q(main_actor__name=actor_name)
        if author_name:
            filters &= Q(main_author__name=author_name)
        return filters


class MovieRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MovieDetailSerializer

    def get(self, request, movie_id: int = None) -> Response:
        try:
            movie_detail = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response(
                "Movie does not exist!", status=status.HTTP_400_BAD_REQUEST
            )
        serializer_class = MovieDetailSerializer(movie_detail, many=False)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def patch(self, request, movie_id: int = None) -> Response:
        try:
            title = request.data["title"]
            category = request.data["category"]
            synopsis = request.data["synopsis"]
            publication_date = request.data["publication_date"]
            main_actor = request.data["main_actor"]
            main_author = request.data["main_author"]
            score = request.data["score"]
        except AssertionError as e:
            return Response(
                f"An error occured {e}!", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            movie_detail = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response(
                f"Movie does not exist!", status=status.HTTP_400_BAD_REQUEST
            )
        serializer_class = MovieDetailSerializer(
            movie_detail, data=request.data, partial=False
        )
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(
                serializer_class.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer_class.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, movie_id: int = None) -> Response:
        try:
            movie_detail = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response(
                f"Movie does not exist!", status=status.HTTP_400_BAD_REQUEST
            )
        try:
            movie_detail.delete()
            return Response(
                f"Movie has been deleted successfully!",
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                f"An error occured {e}!", status=status.HTTP_400_BAD_REQUEST
            )


class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer

    def get(self, request) -> Response:
        categories = Category.objects.all()
        serializer_class = CategorySerializer(categories, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def post(self, request) -> Response:
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddActorToMovieView(generics.CreateAPIView):
    serializer_class = MovieSerializer

    def post(self, request, movie_id: int = None) -> Response:
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response(
                "Movie does not exist!", status=status.HTTP_400_BAD_REQUEST
            )
        try:
            actor_list = request.data["actor_list"]
            type(actor_list) == list
        except AssertionError as e:
            return Response(
                f"Invalid data type: {e}!", status=status.HTTP_400_BAD_REQUEST
            )
        try:
            self.add_actor(movie_id=movie_id, actor_list=actor_list)
            return Response(
                f"Actors {actor_list} has been added successfully to {movie.title}"
            )
        except Exception as e:
            return Response(
                f"An exception occured {e}!", status=status.HTTP_400_BAD_REQUEST
            )

    @classmethod
    def add_actor(cls, movie_id: int, actor_list: list) -> bool:
        movie = Movie.objects.get(id=movie_id)
        for actor in actor_list:
            movie.main_actor.add(actor)
            movie.save()
        return True


class AddAuthorToMovieView(generics.CreateAPIView):
    serializer_class = MovieSerializer

    def post(self, request, movie_id: int = None) -> Response:
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response(
                "Movie does not exist!", status=status.HTTP_400_BAD_REQUEST
            )
        try:
            author_list = request.data["author_list"]
            type(author_list) == list
        except AssertionError as e:
            return Response(
                f"Invalid data type: {e}!", status=status.HTTP_400_BAD_REQUEST
            )
        try:
            self.add_author(movie_id=movie_id, author_list=author_list)
            return Response(
                f"Actors {author_list} has been added successfully to {movie.title}"
            )
        except Exception as e:
            return Response(
                f"An exception occured {e}!", status=status.HTTP_400_BAD_REQUEST
            )

    @classmethod
    def add_author(cls, movie_id: int, author_list: list) -> bool:
        movie = Movie.objects.get(id=movie_id)
        for author in author_list:
            movie.main_author.add(author)
            movie.save()
        return True
