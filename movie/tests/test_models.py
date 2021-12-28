import pytest

from movie.models import Category


class Test_models:
    @pytest.mark.django_db
    def test_create_category(self):
        len0 = Category.objects.all().count()
        category_obj = Category.objects.create(category_name="Test category")
        len1 = Category.objects.all().count()
        assert len1 > len0, 1 > 0
        assert Category.objects.get(id=1).category_name == "Test category"
