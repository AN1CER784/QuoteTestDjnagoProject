from django.db import models


class SourceQuerySet(models.QuerySet):
    def with_quotes_count(self):
        return self.annotate(quotes_count=models.Count('quote'))


class Source(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    objects = SourceQuerySet.as_manager()
