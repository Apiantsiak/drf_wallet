from django.contrib import admin

from .models import Wallets


class CustomWalletAdmin(admin.ModelAdmin):
    model = Wallets
    list_display = (
        "user",
        "wallet_name",
        "currency",
        "card_type",
        "balance",
        "created_at",
        "updated_at",
    )
    list_display_links = ()
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Wallets, CustomWalletAdmin)
