from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from netbox.filters import MultiValueCharFilter, MultiValueNumberFilter
from .models import StorageDevice, StorageBay, RAIDGroup, StorageDeviceHistory

class StorageDeviceFilterSet(NetBoxModelFilterSet):
    device_id = MultiValueNumberFilter(
        field_name='device_id'
    )
    bay_id = MultiValueNumberFilter(
        field_name='bay_id'
    )
    status = MultiValueCharFilter(
        field_name='status'
    )
    manufacturer = MultiValueCharFilter(
        field_name='manufacturer'
    )

    class Meta:
        model = StorageDevice
        fields = ('name', 'storage_device_type', 'serial_number', 'model_number', 'manufacturer', 'status', 'device_id', 'bay_id', 'comments')

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(serial_number__icontains=value) |
            Q(model_number__icontains=value) |
            Q(manufacturer__icontains=value) |
            Q(comments__icontains=value)
        )

class StorageBayFilterSet(NetBoxModelFilterSet):
    device_id = MultiValueNumberFilter(
        field_name='device_id'
    )
    bay_number = MultiValueCharFilter(
        field_name='bay_number'
    )

    class Meta:
        model = StorageBay
        fields = ('device_id', 'bay_number', 'name')

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(bay_number__icontains=value) |
            Q(name__icontains=value)
        )

class RAIDGroupFilterSet(NetBoxModelFilterSet):
    device_id = MultiValueNumberFilter(
        field_name='device_id'
    )
    raid_level = MultiValueCharFilter(
        field_name='raid_level'
    )
    name = MultiValueCharFilter(
        field_name='name'
    )

    class Meta:
        model = RAIDGroup
        fields = ('name', 'device_id', 'raid_level', 'description')

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value)
        )

class StorageDeviceHistoryFilterSet(NetBoxModelFilterSet):
    storage_device_id = MultiValueNumberFilter(
        field_name='storage_device_id'
    )
    status = MultiValueCharFilter(
        field_name='status'
    )
    device_id = MultiValueNumberFilter(
        field_name='device_id'
    )
    replaced_at = MultiValueCharFilter(
        field_name='replaced_at'
    )

    class Meta:
        model = StorageDeviceHistory
        fields = ('storage_device_id', 'status', 'device_id', 'replaced_by', 'replaced_at', 'notes')

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(notes__icontains=value)
        )
