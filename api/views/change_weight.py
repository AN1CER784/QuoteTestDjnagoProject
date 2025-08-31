from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from api.mixins import QuoteAPIMixin


class ChangeWeightView(LoginRequiredMixin, QuoteAPIMixin, View):
    """API для изменение веса цитаты в dashboard"""
    permission_required = 'quotes.change_quote'

    def post(self, request, *args, **kwargs):
        quote = self.get_quote(request)
        try:
            weight = request.POST.get('weight')
            quote.weight = weight
            quote.save()
            return JsonResponse({'success': True, 'message': 'Вес цитаты успешно изменен.'})
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Неверный формат веса.'}, status=400)
