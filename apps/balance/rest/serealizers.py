from rest_framework import serializers
from django.contrib.auth.models import User


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
