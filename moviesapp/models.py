from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=70, default='movie name')
    director_name = models.CharField(max_length=70, default='director name')
    poster = models.URLField(default='google.com')


class Comment(models.Model):
    writer = models.CharField(max_length=70, default='Username')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    comment_in_english = models.CharField(max_length=700)
    comment_in_german = models.CharField(max_length=700)
    comment_in_french = models.CharField(max_length=700)

