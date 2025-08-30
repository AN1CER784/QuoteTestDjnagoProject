from django.db import models


class CategoryQuerySet(models.QuerySet):
    """
    Кастомные методы для выборки категорий:
    - with_quotes_count: добавляет количество цитат в категории
    - with_sources_count: добавляет количество источников в категории
    """
    def with_quotes_count(self):
        return self.annotate(quotes_count=models.Count('source__quote', distinct=True))

    def with_sources_count(self):
        return self.annotate(sources_count=models.Count('source', distinct=True))


class Category(models.Model):
    """
    Модель категории.
    Связи:
    - Один ко многим с Source (много источников - одна категория)
    """
    name = models.CharField(max_length=100)

    objects = CategoryQuerySet.as_manager()

    def __str__(self):
        return self.name
