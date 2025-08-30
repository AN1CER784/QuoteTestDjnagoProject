from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View

from api.services import process_vote


class SetVoteView(LoginRequiredMixin,View):
    def post(self, request, pk):
        """API для выставления голоса (лайка/дизлайка) за цитату"""
        value = request.POST.get('value')
        if not value:
            return JsonResponse({'status': 'error', 'message': 'Не указано значение голоса'}, status=400)

        try:
            value = int(value)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Неверный формат голоса'}, status=400)

        status, quote, message = process_vote(request.user, pk, value)

        if status == 'error':
            return JsonResponse({'status': 'error', 'message': message}, status=404)

        item_html = render_to_string('quotes/includes/quote_card.html', {'quote': quote}, request=request)
        return JsonResponse({
            'success': 'True',
            'item_html': item_html,
            'message': message
        })
