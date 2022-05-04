from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from movie.models import Category, Movie
from movie.serializers import (
    CategorySerializer,
    MovieDetailSerializer,
    MovieSerializer,
    MovieStatisticSerializer,
)


def verify_request(request):
    if request.method == "POST":
        if (
            "title" not in request.data
            or "category" not in request.data
            or "synopsis" not in request.data
            or "publication_date" not in request.data
            or "main_actor" not in request.data
            or "main_author" not in request.data
        ):
            return False
        return True
    if request.method == "PATCH":
        if (
            "title" not in request.data
            and "category_id" not in request.data
            and "synopsis" not in request.data
            and "publication_date" not in request.data
            and "author_id" not in request.data
            and "actor_id" not in request.data
        ):
            return False
        return True


class MovieListCreateView(generics.ListCreateAPIView):
    serializer_class = MovieSerializer

    def post(self, request) -> Response:
        if verify_request(request):
            serializer = MovieSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                f"Invalid Request!", status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request) -> Response:
        movies = Movie.objects.all()
        if len(movies) == 0:
            return Response(
                "There is no movie in the database!", status=status.HTTP_200_OK
            )
        serializer_class = MovieSerializer(movies, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)


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
        if not verify_request(request):
            return Response(
                f"No field has been informed!",
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            movie_detail = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response(
                f"Movie does not exist!", status=status.HTTP_400_BAD_REQUEST
            )
        try:
            if request.data["category_id"]:
                category = request.data["category_id"]
                movie_detail.category = Category.objects.get(id=category)
            if request.data["author_id"]:
                author = request.data["author_id"]
                movie_detail.main_author.clear()
                movie_detail.main_author.add(author)
            if request.data["actor_id"]:
                actor = request.data["actor_id"]
                movie_detail.main_actor.clear()
                movie_detail.main_actor.add(actor)
            # create the context to return the updated actor and author
            context = {
                "title": request.query_params.get("title", None)
                or Movie.objects.get(id=movie_id).title,
                "category": Category.objects.get(id=category).category_name
                or Movie.objects.get(id=movie_id).category.category_name,
                "synopsis": request.query_params.get("synopsis", None)
                or Movie.objects.get(id=movie_id).synopsis,
                "actor": Movie.objects.get(id=movie_id)
                .main_actor.all()[0]
                .name,
                "author": Movie.objects.get(id=movie_id)
                .main_author.all()[0]
                .name,
            }
        except Exception as e:
            return Response(
                "An error has occurred" + str(e),
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer_class = MovieDetailSerializer(
            movie_detail, data=request.data, partial=True
        )
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(context, status=status.HTTP_201_CREATED)
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
        if len(categories) == 0:
            return Response(
                "There is no movie in the database!", status=status.HTTP_200_OK
            )
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


class MovieStatisticView(generics.RetrieveAPIView):
    serializer_class = MovieStatisticSerializer

    def get(self, request) -> Response:
        movies = Movie.objects.all()
        serializer_class = MovieStatisticSerializer(movies, many=False)
        return Response(serializer_class.data, status=status.HTTP_200_OK)
