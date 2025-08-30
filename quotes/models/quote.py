import random

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction


class QuoteQuerySet(models.QuerySet):
    """
    Кастомные методы для выборки цитат:
    - get_random_weighted: возвращает случайную цитату с учетом её веса
    - with_votes: добавляет количество лайков и дизлайков для каждой цитаты
    """
    def get_random_weighted(self):
        quotes = list(self.all())
        if not quotes:
            return None
        weights = [q.weight for q in quotes]
        return random.choices(quotes, weights=weights, k=1)[0]

    def with_votes(self):
        quotes = self.annotate(
            likes=models.Count('vote__value', filter=models.Q(vote__value=1)),
            dislikes=models.Count('vote__value', filter=models.Q(vote__value=-1)),
        )
        return quotes


class Quote(models.Model):
    """
    Модель цитаты.
    Связи:
    - Many-to-One с Source (много цитат - один источник)
    - Many-to-One с User (много цитат - один пользователь)
    """
    text = models.TextField()
    source = models.ForeignKey('Source', on_delete=models.CASCADE)
    weight = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    views = models.PositiveIntegerField(default=0)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    objects = QuoteQuerySet.as_manager()

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self.pk:
                qs = Quote.objects.select_for_update().filter(source=self.source)
                if qs.count() >= 3:
                    raise ValidationError("У этого источника уже 3 цитаты — нельзя добавить ещё.")
            super().save(*args, **kwargs)

    class Meta:
        unique_together = ('text', 'source')