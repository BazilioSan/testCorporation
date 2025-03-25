from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from e_net.models import NetworkNode
from e_net.serializers import NetworkNodeSerializer
from e_net.permissions import IsActiveEmployee


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = (
        NetworkNode.objects.all()
        .select_related("contact", "supplier")
        .prefetch_related("products")
    )
    serializer_class = NetworkNodeSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveEmployee]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["contact__country"]
    search_fields = ["name", "contact__city", "contact__country"]
    ordering_fields = ["created_at", "debt"]
    ordering = ["-created_at"]
