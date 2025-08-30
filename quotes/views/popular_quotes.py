from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from quotes.models import Quote


class PopularQuotesView(LoginRequiredMixin, ListView):
    """View 10 самых популярный цитат по лайкам, дизлайкам и весу"""
    model = Quote
    template_name = 'quotes/popular.html'
    context_object_name = 'quotes'

    def get_queryset(self):
        return Quote.objects.with_votes().order_by('-likes', '-dislikes', '-weight')[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Популярные цитаты'
        return context
