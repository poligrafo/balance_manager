from django.contrib import admin

from apps.balance.models import Balance, Transaction


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    """Admin interface for Balance model."""
    list_display = ('user', 'balance',)
    search_fields = ('user__username',)
    list_filter = ('user',)
    ordering = ('user',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin interface for Transaction model."""
    list_display = ('from_user', 'to_user', 'amount', 'created_at',)
    search_fields = ('from_user__username', 'to_user__username',)
    list_filter = ('transaction_type', 'created_at',)
    ordering = ('-created_at',)

    def get_queryset(self, request):
        """Customize the queryset to show only relevant transactions."""
        queryset = super().get_queryset(request)
        return queryset.select_related('from_user', 'to_user')
