from typing import Optional

from django.db import transaction
from django.contrib.auth.models import User

from apps.balance.models import Balance, Transaction


class InsufficientBalanceException(Exception):
    """Exception raised when there are insufficient funds for a transaction."""
    pass


class BalanceService:
    def __init__(self, user: User):
        self.user = user
        self.balance = self._get_or_create_user_balance()

    def _get_or_create_user_balance(self) -> Balance:
        """Get or create a balance record for the user."""
        balance, _ = Balance.objects.get_or_create(user=self.user)
        return balance

    @transaction.atomic
    def deposit(self, amount: int) -> None:
        """Deposit an amount into the user's balance."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance.balance += amount
        self.balance.save()
        self._log_transaction(amount, transaction_type='deposit')

    @transaction.atomic
    def transfer(self, recipient: User, amount: int) -> None:
        """Transfer an amount from the user's balance to another user's balance."""
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")
        if self.balance.balance < amount:
            raise InsufficientBalanceException("Insufficient funds for transfer.")

        recipient_balance_service = BalanceService(recipient)
        self.balance.balance -= amount
        recipient_balance_service.balance.balance += amount
        self.balance.save()
        recipient_balance_service.balance.save()

        # Log transactions for both users
        self._log_transaction(-amount, recipient, transaction_type='transfer')  # For the sender
        recipient_balance_service._log_transaction(amount, self.user, transaction_type='transfer')  # For the recipient

    def get_balance_in_rub(self) -> float:
        """Get the user's balance in rubles."""
        return self.balance.balance / 100.0

    def _log_transaction(self, amount: int, to_user: Optional[User] = None, transaction_type: str = 'deposit') -> None:
        """Log a transaction for the user."""
        Transaction.objects.create(
            from_user=self.user,
            to_user=to_user,
            transaction_type=transaction_type,
            amount=amount
        )
