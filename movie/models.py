from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from person.models import Actor, Author


class Category(models.Model):
    category_name = models.CharField(max_length=200)


class Movie(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    synopsis = models.TextField(default="Sinópse do filme")
    publication_date = models.DateField()
    main_actor = models.ManyToManyField(Actor)
    main_author = models.ManyToManyField(Author)
    score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
    )
