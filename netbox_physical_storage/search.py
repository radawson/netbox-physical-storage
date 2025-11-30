from netbox.search import SearchIndex, register_search
from .models import StorageDevice, StorageBay, RAIDGroup, StorageDeviceHistory

@register_search
class StorageDeviceIndex(SearchIndex):
    model = StorageDevice
    fields = (
        ('name', 100),
        ('storage_device_type', 50),
        ('serial_number', 50),
        ('model_number', 50),
        ('manufacturer', 50),
        ('comments', 50),
    )

@register_search
class StorageBayIndex(SearchIndex):
    model = StorageBay
    fields = (
        ('bay_number', 100),
        ('name', 50),
    )

@register_search
class RAIDGroupIndex(SearchIndex):
    model = RAIDGroup
    fields = (
        ('name', 100),
        ('raid_level', 50),
        ('description', 50),
    )

@register_search
class StorageDeviceHistoryIndex(SearchIndex):
    model = StorageDeviceHistory
    fields = (
        ('notes', 100),
    )
