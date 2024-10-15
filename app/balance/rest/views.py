import logging

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from app.balance.rest.serealizers import DepositSerializer, TransferSerializer
from app.balance.services import BalanceService, InsufficientBalanceException

logger = logging.getLogger('balance')


class BalanceViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'deposit':
            return DepositSerializer
        if self.action == 'transfer':
            return TransferSerializer
        return None

    def retrieve(self, request):
        balance_service = BalanceService(request.user)
        balance = balance_service.get_balance_in_rub()

        logger.info(f"User {request.user.username} checked balance: {balance} RUB")
        return Response({"balance_rub": balance}, status=status.HTTP_200_OK)

    def deposit(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        balance_service = BalanceService(request.user)
        try:
            balance_service.deposit(amount)
            logger.info(f"User {request.user.username} deposited {amount} копеек")
            return Response({"message": "Баланс успешно пополнен"}, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.error(f"Deposit failed for {request.user.username}: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def transfer(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        recipient = serializer.validated_data['to_user_id']
        amount = serializer.validated_data['amount']
        balance_service = BalanceService(request.user)
        try:
            balance_service.transfer(recipient, amount)
            logger.info(f"User {request.user.username} transferred {amount} копеек to {recipient.username}")
            return Response({"message": "Перевод успешно выполнен"}, status=status.HTTP_200_OK)
        except InsufficientBalanceException:
            logger.error(f"Transfer failed: Insufficient funds for {request.user.username}")
            return Response({"error": "Недостаточно средств"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            logger.error(f"Transfer failed for {request.user.username}: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)