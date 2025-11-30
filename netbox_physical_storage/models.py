from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from django.urls import reverse

class StorageDeviceTypeChoices(ChoiceSet):
    key = 'StorageDevice.type'

    CHOICES = [
        ('SAS', 'SAS', 'blue'),
        ('SATA', 'SATA', 'indigo'),
        ('NVMe', 'NVMe', 'purple'),
    ]

class RAIDLevelChoices(ChoiceSet):
    key = 'RAIDGroup.raid_level'

    CHOICES = [
        ('RAID0', 'RAID 0', 'red'),
        ('RAID1', 'RAID 1', 'green'),
        ('RAID2', 'RAID 2', 'yellow'),
        ('RAID3', 'RAID 3', 'yellow'),
        ('RAID4', 'RAID 4', 'yellow'),
        ('RAID5', 'RAID 5', 'blue'),
        ('RAID6', 'RAID 6', 'purple'),
        ('RAID10', 'RAID 10', 'cyan'),
        ('RAID01', 'RAID 01', 'orange'),
        ('RAID50', 'RAID 50', 'indigo'),
        ('RAID60', 'RAID 60', 'pink'),
    ]

class StorageDeviceStatusChoices(ChoiceSet):
    key = 'StorageDevice.status'

    CHOICES = [
        ('active', 'Active', 'green'),
        ('replaced', 'Replaced', 'orange'),
        ('removed', 'Removed', 'gray'),
        ('failed', 'Failed', 'red'),
        ('spare', 'Spare', 'blue'),
    ]

class StorageBay(NetBoxModel):
    device = models.ForeignKey(
        to='dcim.Device',
        on_delete=models.CASCADE,
        related_name='storage_bays',
        help_text='The enclosure device (e.g., Dell MD1400)'
    )
    bay_number = models.CharField(
        max_length=50,
        help_text='Bay or slot identifier (e.g., "0", "1", "Bay 0", "Slot A1")'
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        help_text='Optional descriptive name for this bay'
    )

    class Meta:
        ordering = ('device', 'bay_number')
        unique_together = ('device', 'bay_number')
        verbose_name = 'Storage Bay'
        verbose_name_plural = 'Storage Bays'

    def __str__(self):
        if self.name:
            return f"{self.device} - {self.name} ({self.bay_number})"
        return f"{self.device} - Bay {self.bay_number}"
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_physical_storage:storagebay', args=[self.pk])

class RAIDGroup(NetBoxModel):
    name = models.CharField(
        max_length=100,
        help_text='Name for this RAID group'
    )
    device = models.ForeignKey(
        to='dcim.Device',
        on_delete=models.CASCADE,
        related_name='raid_groups',
        help_text='The enclosure device containing this RAID'
    )
    raid_level = models.CharField(
        max_length=20,
        choices=RAIDLevelChoices,
        help_text='RAID level configuration'
    )
    description = models.TextField(
        blank=True,
        help_text='Optional description or configuration details'
    )
    storage_devices = models.ManyToManyField(
        to='StorageDevice',
        related_name='raid_groups',
        blank=True,
        help_text='Storage devices in this RAID group'
    )

    class Meta:
        ordering = ('device', 'name')
        verbose_name = 'RAID Group'
        verbose_name_plural = 'RAID Groups'

    def __str__(self):
        return f"{self.name} ({self.raid_level})"
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_physical_storage:raidgroup', args=[self.pk])
    
    def get_raid_level_color(self):
        return RAIDLevelChoices.colors.get(self.raid_level)
    
    def get_drive_count(self):
        """Get number of drives in the RAID"""
        return self.storage_devices.count()
    
    def get_min_drive_size(self):
        """Get smallest drive size in GB for capacity calculations"""
        drives = self.storage_devices.filter(capacity_gb__isnull=False)
        if drives.exists():
            return min(drive.capacity_gb for drive in drives)
        return None
    
    def calculate_capacity(self):
        """Calculate usable capacity based on RAID level and drive sizes"""
        from .utils import calculate_raid_capacity
        
        drive_count = self.get_drive_count()
        if drive_count == 0:
            return None
        
        min_size = self.get_min_drive_size()
        if min_size is None:
            return None
        
        # Get all drive sizes
        drive_sizes = [drive.capacity_gb for drive in self.storage_devices.filter(capacity_gb__isnull=False)]
        
        return calculate_raid_capacity(self.raid_level, drive_sizes, drive_count)
    
    def calculate_failure_tolerance(self):
        """Calculate how many drives can fail before data loss"""
        from .utils import calculate_raid_failure_tolerance
        
        drive_count = self.get_drive_count()
        if drive_count == 0:
            return None
        
        return calculate_raid_failure_tolerance(self.raid_level, drive_count)

class StorageDeviceHistory(NetBoxModel):
    storage_device = models.ForeignKey(
        to='StorageDevice',
        on_delete=models.CASCADE,
        related_name='history_records',
        help_text='The storage device being tracked'
    )
    status = models.CharField(
        max_length=20,
        choices=StorageDeviceStatusChoices,
        help_text='Status at time of change'
    )
    replaced_by = models.ForeignKey(
        to='StorageDevice',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replacement_history',
        help_text='The storage device that replaced this one (if replaced)'
    )
    replaced_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When the replacement occurred'
    )
    notes = models.TextField(
        blank=True,
        help_text='Additional notes about this change'
    )
    device = models.ForeignKey(
        to='dcim.Device',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='storage_device_history',
        help_text='Device the storage device was in at time of change'
    )
    bay = models.ForeignKey(
        to='StorageBay',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='storage_device_history',
        help_text='Bay the storage device was in at time of change'
    )

    class Meta:
        ordering = ('-replaced_at', '-created')
        verbose_name = 'Storage Device History'
        verbose_name_plural = 'Storage Device History'
    
    def __str__(self):
        return f"{self.storage_device} - {self.get_status_display()} ({self.replaced_at or self.created})"
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_physical_storage:storagedevicehistory', args=[self.pk])
    
    def get_status_color(self):
        return StorageDeviceStatusChoices.colors.get(self.status)

class StorageDevice(NetBoxModel):
    name = models.CharField(
        max_length=100
    )
    storage_device_type = models.CharField(
        max_length=100,
        choices=StorageDeviceTypeChoices
    )
    serial_number = models.CharField(
        max_length=100,
        blank=True,
        help_text='Drive serial number (can be added later)'
    )
    model_number = models.CharField(
        max_length=100,
        blank=True,
        help_text='Drive model or manufacturer part number'
    )
    manufacturer = models.CharField(
        max_length=100,
        blank=True,
        help_text='Drive manufacturer'
    )
    capacity_gb = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text='Drive capacity in GB (for RAID calculations)'
    )
    device = models.ForeignKey(
        to='dcim.Device',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='storage_devices',
        help_text='The enclosure device (e.g., Dell MD1400)'
    )
    bay = models.ForeignKey(
        to='StorageBay',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='storage_devices',
        help_text='Physical bay or slot location within the enclosure'
    )
    status = models.CharField(
        max_length=20,
        choices=StorageDeviceStatusChoices,
        default='active',
        help_text='Current status of the storage device'
    )
    replaced_by = models.ForeignKey(
        to='self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replaced_devices',
        help_text='The storage device that replaced this one'
    )
    comments = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_physical_storage:storagedevice', args=[self.pk])
    
    def get_storage_device_type_color(self):
        return StorageDeviceTypeChoices.colors.get(self.storage_device_type)
    
    def get_status_color(self):
        return StorageDeviceStatusChoices.colors.get(self.status)
    
    def get_replacement_history(self):
        """Get all historical records for this device"""
        return self.history_records.all()
    
    def is_active(self):
        """Check if drive is currently active"""
        return self.status == 'active'
