from django.db.models import F

from quotes.models import Quote


def set_seen(request, pk):
    """Прибавляем просмотр к цитате и добавляем по ключу seen_quote pk этой цитаты для защиты от накрутки"""
    seen = request.session.get('seen_quotes', set())
    if not isinstance(seen, set):
        seen = set(seen)
    if str(pk) not in seen:
        Quote.objects.filter(pk=pk).update(views=F('views') + 1)
        seen.add(str(pk))
        request.session['seen_quotes'] = list(seen)
