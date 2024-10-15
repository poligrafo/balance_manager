from rest_framework import serializers
from django.contrib.auth.models import User


class DepositSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1, help_text="Сумма пополнения в копейках")


class TransferSerializer(serializers.Serializer):
    to_user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    amount = serializers.IntegerField(min_value=1, help_text="Сумма перевода в копейках")
