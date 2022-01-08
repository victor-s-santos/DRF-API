from datetime import date

from django.urls import reverse

import pytest

from person.models import Actor, Author


path_list_200 = [("movies", 200), ("categories", 200)]

path_list_empty_content = [
    ("movies", "There is no movie in the database!"),
    ("categories", "There is no category in the database!"),
]

path_list_content = [("categories", "Category Test")]


class Test_get_request:
    @pytest.mark.django_db
    @pytest.mark.parametrize("path, status_code", path_list_200)
    def test_get_movie_endpoints(self, api_client, path, status_code):
        """Must return status_code 200"""
        url = reverse(path)
        assert api_client.get(url).status_code == status_code

    @pytest.mark.django_db
    @pytest.mark.parametrize("path, status_code", path_list_empty_content)
    def test_get_movie_content(self, api_client, path, status_code):
        """Must return status_code 200"""
        url = reverse(path)
        assert api_client.get(url).data == "There is no movie in the database!"

    @pytest.mark.django_db
    def test_post_category(self, api_client):
        url = reverse("categories")
        data = {"category_name": "Terror"}
        response = api_client.post(url, data)
        assert response.status_code == 201

    @pytest.mark.django_db
    @pytest.mark.parametrize("path, content", path_list_content)
    def test_get_category_content(
        self, api_client, path, content, category_obj
    ):
        """Must return status_code 200"""
        url = reverse(path)
        data = [{"category_name": content}]
        assert api_client.get(url).data == data

    @pytest.mark.django_db
    def test_post_movie(self, api_client, category_obj, actor_obj, author_obj):
        url = reverse("movies")
        data = {
            "title": "Title test",
            "category": category_obj.id,
            "synopsis": "Test synopsis",
            "main_author": author_obj.id,
            "main_actor": actor_obj.id,
            "publication_date": date.today(),
        }
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert (
            Actor.objects.get(id=response.data["main_actor"][0]).name
            == "Actor Test"
        )
        assert (
            Author.objects.get(id=response.data["main_author"][0]).name
            == "Author Test"
        )
