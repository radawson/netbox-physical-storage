from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import StorageDevice, StorageBay, RAIDGroup, StorageDeviceHistory

class StorageDeviceSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_physical_storage-api:storagedevice-detail'
    )
    device = serializers.SerializerMethodField()
    bay = serializers.SerializerMethodField()
    replaced_by = serializers.SerializerMethodField()
    replacement_history_count = serializers.SerializerMethodField()
    
    class Meta:
        model = StorageDevice
        fields = [
            'id', 'url', 'name', 'storage_device_type', 'serial_number', 'model_number',
            'manufacturer', 'capacity_gb', 'device', 'bay', 'status', 'replaced_by',
            'replacement_history_count', 'comments', 'tags', 'custom_fields', 'created',
            'last_updated',
        ]
    
    def get_device(self, obj):
        if obj.device:
            return {
                'id': obj.device.id,
                'url': obj.device.get_absolute_url(),
                'display': str(obj.device)
            }
        return None
    
    def get_bay(self, obj):
        if obj.bay:
            return {
                'id': obj.bay.id,
                'url': obj.bay.get_absolute_url(),
                'display': str(obj.bay)
            }
        return None
    
    def get_replaced_by(self, obj):
        if obj.replaced_by:
            return {
                'id': obj.replaced_by.id,
                'url': obj.replaced_by.get_absolute_url(),
                'display': str(obj.replaced_by)
            }
        return None
    
    def get_replacement_history_count(self, obj):
        return obj.get_replacement_history().count()

class NestedStorageDeviceSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_physical_storage-api:storagedevice-detail'
    )

    class Meta:
        model = StorageDevice
        fields = ('id', 'url', 'display', 'name')

class StorageBaySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_physical_storage-api:storagebay-detail'
    )
    device = serializers.SerializerMethodField()
    storage_device_count = serializers.SerializerMethodField()
    
    class Meta:
        model = StorageBay
        fields = [
            'id', 'url', 'device', 'bay_number', 'name', 'storage_device_count',
            'tags', 'custom_fields', 'created', 'last_updated',
        ]
    
    def get_device(self, obj):
        if obj.device:
            return {
                'id': obj.device.id,
                'url': obj.device.get_absolute_url(),
                'display': str(obj.device)
            }
        return None
    
    def get_storage_device_count(self, obj):
        return obj.storage_devices.count()

class NestedStorageBaySerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_physical_storage-api:storagebay-detail'
    )

    class Meta:
        model = StorageBay
        fields = ('id', 'url', 'display', 'bay_number')

class RAIDGroupSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_physical_storage-api:raidgroup-detail'
    )
    device = serializers.SerializerMethodField()
    storage_devices = NestedStorageDeviceSerializer(many=True, read_only=True)
    calculated_capacity = serializers.SerializerMethodField()
    failure_tolerance = serializers.SerializerMethodField()
    drive_count = serializers.SerializerMethodField()
    
    class Meta:
        model = RAIDGroup
        fields = [
            'id', 'url', 'name', 'device', 'raid_level', 'description',
            'storage_devices', 'calculated_capacity', 'failure_tolerance',
            'drive_count', 'tags', 'custom_fields', 'created', 'last_updated',
        ]
    
    def get_device(self, obj):
        if obj.device:
            return {
                'id': obj.device.id,
                'url': obj.device.get_absolute_url(),
                'display': str(obj.device)
            }
        return None
    
    def get_calculated_capacity(self, obj):
        result = obj.calculate_capacity()
        if result:
            return result.get('formatted')
        return None
    
    def get_failure_tolerance(self, obj):
        result = obj.calculate_failure_tolerance()
        if result:
            return result.get('description')
        return None
    
    def get_drive_count(self, obj):
        return obj.get_drive_count()

class StorageDeviceHistorySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_physical_storage-api:storagedevicehistory-detail'
    )
    storage_device = serializers.SerializerMethodField()
    replaced_by = serializers.SerializerMethodField()
    device = serializers.SerializerMethodField()
    bay = serializers.SerializerMethodField()
    
    class Meta:
        model = StorageDeviceHistory
        fields = [
            'id', 'url', 'storage_device', 'status', 'replaced_by', 'replaced_at',
            'device', 'bay', 'notes', 'tags', 'custom_fields', 'created', 'last_updated',
        ]
    
    def get_storage_device(self, obj):
        if obj.storage_device:
            return {
                'id': obj.storage_device.id,
                'url': obj.storage_device.get_absolute_url(),
                'display': str(obj.storage_device)
            }
        return None
    
    def get_replaced_by(self, obj):
        if obj.replaced_by:
            return {
                'id': obj.replaced_by.id,
                'url': obj.replaced_by.get_absolute_url(),
                'display': str(obj.replaced_by)
            }
        return None
    
    def get_device(self, obj):
        if obj.device:
            return {
                'id': obj.device.id,
                'url': obj.device.get_absolute_url(),
                'display': str(obj.device)
            }
        return None
    
    def get_bay(self, obj):
        if obj.bay:
            return {
                'id': obj.bay.id,
                'url': obj.bay.get_absolute_url(),
                'display': str(obj.bay)
            }
        return None
