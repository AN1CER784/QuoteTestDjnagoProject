from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView

from quotes.models import Source, Category


class DashBoardSourcesView(PermissionRequiredMixin, ListView):
    """View для отображения источников категории в Dashboard после перехода по конкретной категории"""
    model = Source
    template_name = 'dashboard/category_detail.html'
    context_object_name = 'sources'
    slug_url_kwarg = 'category_id'
    permission_required = 'quotes.change_quote'

    def get_queryset(self):
        return Source.objects.filter(category__pk=self.kwargs.get(self.slug_url_kwarg)).with_quotes_count()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Дашборд Источников'
        context['category'] = Category.objects.get(pk=self.kwargs.get(self.slug_url_kwarg))
        return context
