from django.urls import reverse

import pytest
from _pytest.fixtures import fixture


path_list_200 = [("movies", 200), ("categories", 200)]

path_list_empty_content = [
    ("movies", "There is no movie in the database!"),
    ("categories", "There is no category in the database!"),
]

path_list_content = [("categories", "Terror")]


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

    @fixture
    @pytest.mark.django_db
    def test_post_category(self, api_client):
        url = reverse("categories")
        data = {"category_name": "Terror"}
        response = api_client.post(url, data)
        assert response.status_code == 201

    @pytest.mark.django_db
    @pytest.mark.parametrize("path, content", path_list_content)
    def test_get_category_content(
        self, api_client, path, content, test_post_category
    ):
        """Must return status_code 200"""
        url = reverse(path)
        data = [{"category_name": content}]
        assert api_client.get(url).data == data
