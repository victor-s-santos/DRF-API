from django.db import models


class Author(models.Model):
    GENRE_CHOICES = ((1, "Female"), (2, "Male"))
    name = models.CharField(max_length=200)
    genre = models.IntegerField(choices=GENRE_CHOICES, default=1)
    birth_date = models.DateField()
    nationality = models.CharField(max_length=200)

    @property
    def score_average(self):
        """average score of the films this author worked on"""
        author = Author.objects.get(id=self.id)
        try:
            movies = author.movie_set.all()
            list_score = [movie.score for movie in movies]
            avg_score = sum(list_score) / len(list_score)
            return avg_score
        except Exception as e:
            return "An error occured! {e}"


class Actor(models.Model):
    GENRE_CHOICES = ((1, "Female"), (2, "Male"))
    name = models.CharField(max_length=200)
    genre = models.IntegerField(choices=GENRE_CHOICES, default=1)
    birth_date = models.DateField()
    nationality = models.CharField(max_length=200)
