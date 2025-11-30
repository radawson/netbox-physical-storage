import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn
from .models import StorageDevice, StorageBay, RAIDGroup, StorageDeviceHistory

class StorageDeviceTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    storage_device_type = ChoiceFieldColumn()
    device = tables.Column(
        linkify=True
    )
    bay = tables.Column(
        linkify=True
    )
    status = ChoiceFieldColumn()
    model_number = tables.Column()
    capacity_gb = tables.Column()

    class Meta(NetBoxTable.Meta):
        model = StorageDevice
        fields = (
            'pk', 'id', 'name', 'storage_device_type', 'serial_number',
            'model_number', 'manufacturer', 'capacity_gb', 'device', 'bay',
            'status', 'comments'
        )
        default_columns = ('name', 'storage_device_type', 'serial_number', 'device', 'bay', 'status')

class StorageBayTable(NetBoxTable):
    device = tables.Column(
        linkify=True
    )
    bay_number = tables.Column()
    name = tables.Column()
    storage_device_count = tables.Column(
        accessor='storage_devices.count',
        verbose_name='Drives'
    )

    class Meta(NetBoxTable.Meta):
        model = StorageBay
        fields = ('pk', 'id', 'device', 'bay_number', 'name', 'storage_device_count')
        default_columns = ('device', 'bay_number', 'name', 'storage_device_count')

class RAIDGroupTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    device = tables.Column(
        linkify=True
    )
    raid_level = ChoiceFieldColumn()
    drive_count = tables.Column(
        accessor='get_drive_count',
        verbose_name='Drives'
    )
    calculated_capacity = tables.Column(
        accessor='calculate_capacity',
        verbose_name='Capacity',
        orderable=False
    )
    
    def render_calculated_capacity(self, value):
        if value and isinstance(value, dict) and 'formatted' in value:
            return value['formatted']
        return '—'
    
    failure_tolerance = tables.Column(
        accessor='calculate_failure_tolerance',
        verbose_name='Failure Tolerance',
        orderable=False
    )
    
    def render_failure_tolerance(self, value):
        if value and isinstance(value, dict) and 'description' in value:
            return value['description']
        return '—'

    class Meta(NetBoxTable.Meta):
        model = RAIDGroup
        fields = (
            'pk', 'id', 'name', 'device', 'raid_level', 'drive_count',
            'calculated_capacity', 'failure_tolerance', 'description'
        )
        default_columns = ('name', 'device', 'raid_level', 'drive_count', 'calculated_capacity', 'failure_tolerance')

class StorageDeviceHistoryTable(NetBoxTable):
    storage_device = tables.Column(
        linkify=True
    )
    status = ChoiceFieldColumn()
    replaced_by = tables.Column(
        linkify=True
    )
    replaced_at = tables.DateTimeColumn()
    device = tables.Column(
        linkify=True
    )
    bay = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = StorageDeviceHistory
        fields = (
            'pk', 'id', 'storage_device', 'status', 'replaced_by',
            'replaced_at', 'device', 'bay', 'notes', 'created'
        )
        default_columns = ('storage_device', 'status', 'replaced_by', 'replaced_at', 'device', 'bay')
