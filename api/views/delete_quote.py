from django.http import JsonResponse
from django.views import View

from api.mixins import QuoteAPIMixin


class DeleteQuoteView(QuoteAPIMixin, View):
    def post(self, request):
        quote = self.get_quote(request)
        quote.delete()
        return JsonResponse({'success': True, 'message': 'Цитата успешно удалена.'})


