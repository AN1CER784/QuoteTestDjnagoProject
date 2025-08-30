from django.db import models


class SourceQuerySet(models.QuerySet):
    """
    Кастомные методы для выборки источников:
    - with_quotes_count: добавляет количество цитат для каждого источника
    """
    def with_quotes_count(self):
        return self.annotate(quotes_count=models.Count('quote', distinct=True))


class Source(models.Model):
    """
    Модель источника.
    Связи:
    - Many-to-One с Category (много источников - одна категория)
    - Many-to-One с User (много источников - один пользователь)
    """
    name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    objects = SourceQuerySet.as_manager()
