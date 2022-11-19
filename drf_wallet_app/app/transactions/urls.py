from django.urls import path

from .views import (  # isort:skip
    CreateTransactionView,
    TransactionDetailView,
    TransactionListView,
)

urlpatterns = [
    path("", CreateTransactionView.as_view()),
    path("<int:pk>/", TransactionDetailView.as_view()),
    path("<slug:wallet_name>/", TransactionListView.as_view()),
]
