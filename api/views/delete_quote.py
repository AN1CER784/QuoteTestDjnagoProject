from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from api.mixins import QuoteAPIMixin


class DeleteQuoteView(LoginRequiredMixin, QuoteAPIMixin, View):
    """API для удаления цитаты через dashboard"""
    permission_required = 'quotes.delete_quote'

    def post(self, request):
        quote = self.get_quote(request)
        quote.delete()
        return JsonResponse({'success': True, 'message': 'Цитата успешно удалена.'})


