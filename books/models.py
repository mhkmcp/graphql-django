from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200, default='')
    excerpt = models.TextField()

    def __str__(self):
        return self.title
