from django.core.exceptions import ValidationError
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from wallet.models import Wallets

from .models import Transaction
from .serializers import TransactionSerializer

from .services import (  # isort:skip
    check_receiver_wallet_exists,
    filter_user_wallet,
    make_transaction,
)


class CreateTransactionView(generics.ListCreateAPIView):

    serializer_class = TransactionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Transaction.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            sender = filter_user_wallet(self.request.user, request.data["sender"])
            receiver = check_receiver_wallet_exists(request.data["receiver"])
            transactions_amount = request.data["transaction_amount"]
            make_transaction(sender, receiver, transactions_amount)
        except ValidationError as err:
            content = {"error": err.message}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_queryset(self):
        """Return object for current authenticated user only"""
        wallet = Wallets.objects.filter(user=self.request.user)
        return self.queryset.filter(sender__in=wallet).union(
            self.queryset.filter(receiver__in=wallet)
        )


class TransactionListView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        """Return object for current authenticated user only"""
        wallet = Wallets.objects.filter(
            wallet_name=self.kwargs["wallet_name"], user=self.request.user
        )
        return self.queryset.filter(sender__in=wallet).union(
            self.queryset.filter(receiver__in=wallet)
        )


class TransactionDetailView(generics.RetrieveAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
