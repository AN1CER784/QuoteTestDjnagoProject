from django.http import JsonResponse
from django.views import View

from api.mixins import QuoteAPIMixin


class ChangeWeightView(QuoteAPIMixin, View):
    def post(self, request, *args, **kwargs):
        quote = self.get_quote(request)
        weight = request.POST.get('weight')
        quote.weight = weight
        quote.save()
        return JsonResponse({'success': True, 'message': 'Вес цитаты успешно изменен.'})