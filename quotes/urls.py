
from django.urls import path
from .views import RandomQuoteView, AddQuoteView, PopularQuotesView

app_name = 'quotes'
urlpatterns = [

    path('', RandomQuoteView.as_view(), name='index'),
    path('add-quote', AddQuoteView.as_view(), name='add-quote'),
    path('popular-quotes', PopularQuotesView.as_view(), name='popular-quotes'),

]
