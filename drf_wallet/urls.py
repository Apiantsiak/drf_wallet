from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("accounts.urls")),
    path("api/wallet/", include("wallet.urls")),
    path("api/wallets/transactions/", include("transactions.urls")),
]
