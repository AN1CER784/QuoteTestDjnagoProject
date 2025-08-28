from django.contrib.auth import get_user_model

from quotes.models import Quote, Vote

User = get_user_model()


def get_quote_by_id(quote_id: int) -> Quote | None:
    """
    Получает цитату по её идентификатору.
    """
    return Quote.objects.prefetch_related("vote_set").with_votes().filter(pk=quote_id).first()


def process_vote(user: User, quote_id: int, value: int) -> tuple[str, Quote | None, str]:
    """
    Основная бизнес-логика голосования за цитату.
    """
    quote = get_quote_by_id(quote_id)

    if not quote:
        return 'error', None, 'Цитата не найдена'

    vote = Vote.objects.filter(quote=quote, user=user).first()

    if vote is None:
        Vote.objects.create(quote=quote, user=user, value=value)
        message = 'Голос учтён'
    elif vote.value == value:
        vote.delete()
        message = 'Голос удалён'
    else:
        vote.value = value
        vote.save()
        message = 'Голос обновлён'

    quote = Quote.objects.with_votes().get(pk=quote.id)
    return 'ok', quote, message
