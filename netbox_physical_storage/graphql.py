from graphene import ObjectType
from netbox.graphql.types import NetBoxObjectType
from netbox.graphql.fields import ObjectField, ObjectListField
from . import filtersets, models

class StorageDeviceType(NetBoxObjectType):

    class Meta:
        model = models.StorageDevice
        fields = '__all__'

class StorageBayType(NetBoxObjectType):

    class Meta:
        model = models.StorageBay
        fields = '__all__'

class RAIDGroupType(NetBoxObjectType):

    class Meta:
        model = models.RAIDGroup
        fields = '__all__'

class StorageDeviceHistoryType(NetBoxObjectType):

    class Meta:
        model = models.StorageDeviceHistory
        fields = '__all__'

class Query(ObjectType):
    storage_device = ObjectField(StorageDeviceType)
    storage_device_list = ObjectListField(StorageDeviceType)
    storage_bay = ObjectField(StorageBayType)
    storage_bay_list = ObjectListField(StorageBayType)
    raid_group = ObjectField(RAIDGroupType)
    raid_group_list = ObjectListField(RAIDGroupType)
    storage_device_history = ObjectField(StorageDeviceHistoryType)
    storage_device_history_list = ObjectListField(StorageDeviceHistoryType)

schema = Query
