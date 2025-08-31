from django.db.models import F

from quotes.models import Quote


def set_seen(request, pk):
    """Прибавляем просмотр к цитате и добавляем pk в сессию, чтобы не засчитывать повторно"""
    seen = set(request.session.get('seen_quotes', []))
    if str(pk) not in seen:
        Quote.objects.filter(pk=pk).update(views=F('views') + 1)
        seen.add(str(pk))
        request.session['seen_quotes'] = list(seen)
        request.session.modified = True
