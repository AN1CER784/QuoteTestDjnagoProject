from django.urls import path

from .views import DashBoardSourcesView, DashBoardCategoriesView, DashBoardQuotesView

app_name = 'dashboard'

urlpatterns = [

    path('', DashBoardCategoriesView.as_view(), name='categories'),

    path('<int:category_id>/sources', DashBoardSourcesView.as_view(), name='sources'),
    path('<int:category_id>/sources/<int:source_id>/quotes', DashBoardQuotesView.as_view(), name='quotes'),
]
