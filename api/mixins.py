from django.shortcuts import get_object_or_404

from quotes.models import Quote


class QuoteAPIMixin:
    def get_quote(self, request):
        quote_id = request.POST.get('quote_id')
        quote = get_object_or_404(Quote, id=quote_id)
        return quote
