import logging

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView

from quotes.forms import QuoteForm
from quotes.models import Category

logger = logging.getLogger(__name__)


class AddQuoteView(CreateView):
    form_class = QuoteForm
    template_name = 'quotes/add_quote.html'
    success_url = reverse_lazy('quotes:index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Цитата успешно добавлена.')
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить цитату'
        context['categories'] = Category.objects.all()
        return context
