from django.db import models
from django.contrib.auth.models import User


class Balance(models.Model):
    """A model to store the balance of a user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='balance')
    balance = models.BigIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.balance} kopecks"


class Transaction(models.Model):
    """A model representing a transaction."""
    TRANSACTION_CHOICES = [
        ('deposit', 'Deposit'),
        ('transfer', 'Transfer'),
    ]
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outgoing_transactions')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming_transactions', null=True)
    amount = models.BigIntegerField(default=0)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"{self.from_user.username} -> {self.to_user.username if self.to_user else 'self'}: {self.amount} "
                f"kopecks")
