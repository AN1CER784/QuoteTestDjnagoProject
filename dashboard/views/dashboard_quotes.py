from django.views.generic import ListView

from quotes.models import Quote, Source


class DashBoardQuotesView(ListView):
    model = Quote
    template_name = 'dashboard/source_detail.html'
    context_object_name = 'quotes'
    slug_url_kwarg = 'source_id'

    def get_queryset(self):
        return Quote.objects.filter(source_id=self.kwargs.get(self.slug_url_kwarg)).with_votes().order_by('-weight')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Дашборд Цитат'
        context['source'] = Source.objects.get(pk=self.kwargs.get(self.slug_url_kwarg))
        return context
