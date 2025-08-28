from django.urls import path

from .views import SetVoteView, DeleteQuoteView, ChangeWeightView

app_name = 'api'

urlpatterns = [
    path('vote/<int:pk>/', SetVoteView.as_view(), name='vote'),
    path('delete-quote', DeleteQuoteView.as_view(), name='delete-quote'),
    path('change-weight', ChangeWeightView.as_view(), name='change-weight'),
]
