from rest_framework import serializers

from .models import Wallets


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallets
        fields = "__all__"
