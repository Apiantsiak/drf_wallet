from django.urls import include, path

from .views import WalletDetailView, WalletListCreateView

urlpatterns = [
    path("", WalletListCreateView.as_view()),
    path("transactions/", include("transactions.urls")),
    path("<slug:wallet_name>/", WalletDetailView.as_view()),
]
