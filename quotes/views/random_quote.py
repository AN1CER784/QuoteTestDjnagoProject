
from django.views.generic import DetailView

from quotes.models import Quote
from quotes.services import set_seen


class RandomQuoteView(DetailView):
    context_object_name = 'quote'
    template_name = 'quotes/index.html'
    model = Quote

    def get_object(self, queryset=None):
        return Quote.objects.with_votes().get_random_weighted()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Случайная цитата'
        return context

    def get(self, request, *args, **kwargs):
        pk = self.get_object().pk
        set_seen(request, pk)
        return super().get(request, *args, **kwargs)

