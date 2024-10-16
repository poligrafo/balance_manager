import logging

from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.balance.models import Transaction
from apps.balance.rest.serealizers import DepositSerializer, TransferSerializer, TransactionSerializer
from apps.balance.services import BalanceService, InsufficientBalanceException

logger = logging.getLogger('balance')


class BalanceViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return the appropriate serializer class based on the action."""
        if self.action == 'deposit':
            return DepositSerializer
        if self.action == 'transfer':
            return TransferSerializer
        return None

    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            balance_service = BalanceService(user)
            balance_in_rub = balance_service.get_balance_in_rub()
            return Response({"balance": balance_in_rub}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], url_path='deposit')
    def deposit(self, request):
        """Deposit an amount into the user's balance."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        balance_service = BalanceService(request.user)
        try:
            balance_service.deposit(amount)
            logger.info(f"User {request.user.username} deposited {amount} копеек")
            return Response({"message": "Balance successfully replenished"}, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.error(f"Deposit failed for {request.user.username}: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='transfer')
    def transfer(self, request):
        """Transfer an amount from the user's balance to another user's balance."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        recipient = serializer.validated_data['to_user_id']
        amount = serializer.validated_data['amount']
        balance_service = BalanceService(request.user)
        try:
            balance_service.transfer(recipient, amount)
            logger.info(f"User {request.user.username} transferred {amount} копеек to {recipient.username}")
            return Response({"message": "Transfer successfully completed"}, status=status.HTTP_200_OK)
        except InsufficientBalanceException:
            logger.error(f"Transfer failed: Insufficient funds for {request.user.username}")
            return Response({"error": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            logger.error(f"Transfer failed for {request.user.username}: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='transactions')
    def transaction_history(self, request):
        """Get the transaction history for the user."""
        transactions = Transaction.objects.filter(from_user=request.user).order_by('-created_at')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

