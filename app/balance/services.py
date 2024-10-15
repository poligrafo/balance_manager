from typing import Optional

from django.db import transaction
from django.contrib.auth.models import User

from app.balance.models import Balance, Transaction


class InsufficientBalanceException(Exception):
    pass

class BalanceService:
    def __init__(self, user: User):
        self.user = user
        self.balance = self._get_or_create_user_balance()

    def _get_or_create_user_balance(self) -> Balance:
        balance, _ = Balance.objects.get_or_create(user=self.user)
        return balance

    @transaction.atomic
    def deposit(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        self.balance.balance += amount
        self.balance.save()
        self._log_transaction(amount, transaction_type='deposit')

    @transaction.atomic
    def transfer(self, recipient: User, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Сумма перевода должна быть положительной")
        if self.balance.balance < amount:
            raise InsufficientBalanceException("Недостаточно средств для перевода")

        recipient_balance = BalanceService(recipient)
        self.balance.balance -= amount
        recipient_balance.balance.balance += amount
        self.balance.save()
        recipient_balance.balance.save()

        self._log_transaction(amount, recipient, 'transfer')

    def get_balance_in_rub(self) -> float:
        return self.balance.balance / 100.0

    def _log_transaction(self, amount: int, to_user: Optional[User] = None, transaction_type: str = 'deposit') -> None:
        Transaction.objects.create(
            from_user=self.user,
            to_user=to_user,
            transaction_type=transaction_type,
            amount=amount
        )