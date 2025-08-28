from django.db import models


class CategoryQuerySet(models.QuerySet):
    def with_quotes_count(self):
        return self.annotate(quotes_count=models.Count('source__quote'))

    def with_sources_count(self):
        return self.annotate(sources_count=models.Count('source'))


class Category(models.Model):
    name = models.CharField(max_length=100)

    objects = CategoryQuerySet.as_manager()

    def __str__(self):
        return self.name
