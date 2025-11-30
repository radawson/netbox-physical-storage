from .models import (
    StorageDevice, StorageDeviceTypeChoices, StorageDeviceStatusChoices,
    StorageBay, RAIDGroup, RAIDLevelChoices, StorageDeviceHistory
)
from utilities.forms.fields import CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField
from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm

class StorageDeviceFilterForm(NetBoxModelFilterSetForm):
    model = StorageDevice

    storage_device = forms.ModelMultipleChoiceField(
        queryset=StorageDevice.objects.all(),
        required=False
    )

    storage_device_type = forms.MultipleChoiceField(
        choices=StorageDeviceTypeChoices,
        required=False
    )

    status = forms.MultipleChoiceField(
        choices=StorageDeviceStatusChoices,
        required=False
    )

    device_id = forms.ModelMultipleChoiceField(
        queryset=StorageDevice.objects.none(),  # Will be filtered by API
        required=False,
        label='Device'
    )

    bay_id = forms.ModelMultipleChoiceField(
        queryset=StorageBay.objects.all(),
        required=False,
        label='Bay'
    )

    manufacturer = forms.CharField(
        required=False
    )

class StorageDeviceForm(NetBoxModelForm):
    device = DynamicModelChoiceField(
        queryset=None,  # NetBox will set this based on query_params
        query_params={'kind': 'device'},
        required=False,
        label='Enclosure Device'
    )
    bay = DynamicModelChoiceField(
        queryset=StorageBay.objects.all(),
        required=False,
        label='Storage Bay',
        query_params={'device_id': '$device'}
    )
    status = forms.ChoiceField(
        choices=StorageDeviceStatusChoices,
        required=True,
        initial='active'
    )
    model_number = forms.CharField(
        required=False,
        max_length=100
    )
    manufacturer = forms.CharField(
        required=False,
        max_length=100
    )
    capacity_gb = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        help_text='Drive capacity in GB (for RAID calculations)'
    )
    replaced_by = DynamicModelChoiceField(
        queryset=StorageDevice.objects.all(),
        required=False,
        label='Replaced By',
        help_text='The storage device that replaced this one'
    )
    comments = CommentField()

    class Meta:
        model = StorageDevice
        fields = (
            'name', 'storage_device_type', 'serial_number', 'model_number',
            'manufacturer', 'capacity_gb', 'device', 'bay', 'status',
            'replaced_by', 'comments'
        )

class StorageBayFilterForm(NetBoxModelFilterSetForm):
    model = StorageBay

    device_id = forms.ModelMultipleChoiceField(
        queryset=StorageBay.objects.none(),  # Will be filtered by API
        required=False,
        label='Device'
    )

    bay_number = forms.CharField(
        required=False
    )

class StorageBayForm(NetBoxModelForm):
    device = DynamicModelChoiceField(
        queryset=None,  # Will be set by NetBox
        query_params={'kind': 'device'},
        required=True,
        label='Enclosure Device'
    )
    bay_number = forms.CharField(
        required=True,
        max_length=50,
        help_text='Bay or slot identifier (e.g., "0", "1", "Bay 0", "Slot A1")'
    )
    name = forms.CharField(
        required=False,
        max_length=100,
        help_text='Optional descriptive name for this bay'
    )

    class Meta:
        model = StorageBay
        fields = ('device', 'bay_number', 'name')

class RAIDGroupFilterForm(NetBoxModelFilterSetForm):
    model = RAIDGroup

    device_id = forms.ModelMultipleChoiceField(
        queryset=RAIDGroup.objects.none(),  # Will be filtered by API
        required=False,
        label='Device'
    )

    raid_level = forms.MultipleChoiceField(
        choices=RAIDLevelChoices,
        required=False
    )

    name = forms.CharField(
        required=False
    )

class RAIDGroupForm(NetBoxModelForm):
    name = forms.CharField(
        required=True,
        max_length=100
    )
    device = DynamicModelChoiceField(
        queryset=None,  # Will be set by NetBox
        query_params={'kind': 'device'},
        required=True,
        label='Enclosure Device'
    )
    raid_level = forms.ChoiceField(
        choices=RAIDLevelChoices,
        required=True
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea,
        help_text='Optional description or configuration details'
    )
    storage_devices = DynamicModelMultipleChoiceField(
        queryset=StorageDevice.objects.filter(status='active'),
        required=False,
        label='Storage Devices',
        help_text='Storage devices in this RAID group'
    )

    class Meta:
        model = RAIDGroup
        fields = ('name', 'device', 'raid_level', 'description', 'storage_devices')

class StorageDeviceHistoryFilterForm(NetBoxModelFilterSetForm):
    model = StorageDeviceHistory

    storage_device_id = forms.ModelMultipleChoiceField(
        queryset=StorageDevice.objects.all(),
        required=False,
        label='Storage Device'
    )

    status = forms.MultipleChoiceField(
        choices=StorageDeviceStatusChoices,
        required=False
    )

    device_id = forms.ModelMultipleChoiceField(
        queryset=StorageDeviceHistory.objects.none(),  # Will be filtered by API
        required=False,
        label='Device'
    )

    replaced_at_after = forms.DateTimeField(
        required=False,
        label='Replaced After'
    )

    replaced_at_before = forms.DateTimeField(
        required=False,
        label='Replaced Before'
    )
