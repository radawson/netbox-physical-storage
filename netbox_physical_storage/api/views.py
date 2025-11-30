from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import (
    StorageDeviceSerializer, StorageBaySerializer, RAIDGroupSerializer,
    StorageDeviceHistorySerializer
)

class StorageDeviceViewSet(NetBoxModelViewSet):
    queryset = models.StorageDevice.objects.prefetch_related('tags', 'device', 'bay', 'replaced_by')
    serializer_class = StorageDeviceSerializer
    filterset_class = filtersets.StorageDeviceFilterSet

class StorageBayViewSet(NetBoxModelViewSet):
    queryset = models.StorageBay.objects.prefetch_related('tags', 'device')
    serializer_class = StorageBaySerializer
    filterset_class = filtersets.StorageBayFilterSet

class RAIDGroupViewSet(NetBoxModelViewSet):
    queryset = models.RAIDGroup.objects.prefetch_related('tags', 'device', 'storage_devices')
    serializer_class = RAIDGroupSerializer
    filterset_class = filtersets.RAIDGroupFilterSet

class StorageDeviceHistoryViewSet(NetBoxModelViewSet):
    queryset = models.StorageDeviceHistory.objects.prefetch_related('tags', 'storage_device', 'replaced_by', 'device', 'bay')
    serializer_class = StorageDeviceHistorySerializer
    filterset_class = filtersets.StorageDeviceHistoryFilterSet
