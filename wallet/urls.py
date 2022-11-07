from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import WalletDetailView, WalletListCreateView

# router = DefaultRouter()
#
# router.register('account', WalletViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path("", WalletListCreateView.as_view()),
    path("<slug:wallet_name>/", WalletDetailView.as_view()),
]
