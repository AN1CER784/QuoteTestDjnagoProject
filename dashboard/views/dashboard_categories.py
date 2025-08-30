from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView

from quotes.models import Category


class DashBoardCategoriesView(PermissionRequiredMixin, ListView):
    """View для отображения всех категорий в dashboard (фильмы, книги и тд)"""
    model = Category
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'categories'
    permission_required = 'quotes.change_quote'

    def get_queryset(self):
        return Category.objects.with_quotes_count().with_sources_count()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Дашборд категорий'
        return context
