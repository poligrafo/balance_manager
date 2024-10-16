from rest_framework import serializers
from django.contrib.auth.models import User

from apps.balance.models import Transaction


class DepositSerializer(serializers.Serializer):
    """
    Serializer for depositing funds.

    Fields:
        - amount: Deposit amount in kopecks (integer, greater than zero).
    """
    amount = serializers.IntegerField(
        min_value=1,
        help_text="The deposit amount in kopecks. Must be a positive integer."
    )


class TransferSerializer(serializers.Serializer):
    """
    Serializer for transferring funds between users.

    Fields:
        - to_user_id: ID of the transfer recipient (primary key of an existing user).
        - amount: Transfer amount in kopecks (integer, greater than zero).
    """
    to_user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        help_text="ID of the transfer recipient. Specify an existing user."
    )
    amount = serializers.IntegerField(
        min_value=1,
        help_text="The transfer amount in kopecks. Must be a positive integer."
    )


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for transaction history.

    Fields:
        - id: Unique identifier for the transaction.
        - from_user: User who initiated the transaction.
        - to_user: User who received the funds (nullable).
        - transaction_type: Type of the transaction (deposit/transfer).
        - amount: Amount of the transaction in kopecks.
        - created_at: Timestamp when the transaction was created.
    """
    from_user = serializers.StringRelatedField()
    to_user = serializers.StringRelatedField(allow_null=True)

    class Meta:
        model = Transaction
        fields = ['id', 'from_user', 'to_user', 'transaction_type', 'amount', 'created_at']
        read_only_fields = ['id', 'created_at']
