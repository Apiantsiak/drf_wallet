from django.core.exceptions import ValidationError
from rest_framework import generics, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Wallets
from .serializers import WalletSerializer
from .services import check_wallets_quantity, create_wallet_data


class WalletListCreateView(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Wallets.objects.all()
    serializer_class = WalletSerializer

    def get_queryset(self):
        """Return object for current authenticated user only"""
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = create_wallet_data(request)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            check_wallets_quantity(self.request.user)
            self.perform_create(serializer)
        except ValidationError as err:
            content = {"error": err.message}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WalletDetailView(generics.RetrieveDestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Wallets.objects.all()
    serializer_class = WalletSerializer
    lookup_field = "wallet_name"

    def get_queryset(self):
        """Return object for current authenticated user only"""
        return self.queryset.filter(user=self.request.user)
