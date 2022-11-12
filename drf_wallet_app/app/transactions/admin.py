from django.contrib import admin

from .models import Transaction


class CustomTransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = (
        "sender",
        "receiver",
        "transaction_amount",
        "commission",
        "status",
        "created_at",
    )
    list_display_links = ()
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Transaction, CustomTransactionAdmin)
