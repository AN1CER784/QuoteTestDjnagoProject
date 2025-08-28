from django.db.models import F

from quotes.models import Quote


def set_seen(request, pk):
    seen = request.session.get('seen_quotes', set())
    if str(pk) not in seen:
        Quote.objects.filter(pk=pk).update(views=F('views') + 1)
        seen.add(str(pk))
        request.session['seen_quotes'] = set(seen)
