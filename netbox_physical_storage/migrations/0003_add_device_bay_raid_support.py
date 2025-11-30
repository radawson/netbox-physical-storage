# Generated migration for device, bay, and RAID support

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators
import taggit.managers
import utilities.json
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_physical_storage', '0002_remove_storagedevice_mount_point'),
        ('dcim', '__first__'),  # NetBox's dcim app
        ('extras', '__first__'),  # NetBox's extras app
    ]

    operations = [
        # Create StorageBay model
        migrations.CreateModel(
            name='StorageBay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('bay_number', models.CharField(help_text='Bay or slot identifier (e.g., "0", "1", "Bay 0", "Slot A1")', max_length=50)),
                ('name', models.CharField(blank=True, help_text='Optional descriptive name for this bay', max_length=100)),
                ('device', models.ForeignKey(help_text='The enclosure device (e.g., Dell MD1400)', on_delete=django.db.models.deletion.CASCADE, related_name='storage_bays', to='dcim.device')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'Storage Bay',
                'verbose_name_plural': 'Storage Bays',
                'ordering': ('device', 'bay_number'),
            },
        ),
        migrations.AddField(
            model_name='storagedevice',
            name='bay',
            field=models.ForeignKey(blank=True, help_text='Physical bay or slot location within the enclosure', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='storage_devices', to='netbox_physical_storage.storagebay'),
        ),
        migrations.AddField(
            model_name='storagedevice',
            name='capacity_gb',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Drive capacity in GB (for RAID calculations)', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
        migrations.AddField(
            model_name='storagedevice',
            name='device',
            field=models.ForeignKey(blank=True, help_text='The enclosure device (e.g., Dell MD1400)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='storage_devices', to='dcim.device'),
        ),
        migrations.AddField(
            model_name='storagedevice',
            name='manufacturer',
            field=models.CharField(blank=True, help_text='Drive manufacturer', max_length=100),
        ),
        migrations.AddField(
            model_name='storagedevice',
            name='model_number',
            field=models.CharField(blank=True, help_text='Drive model or manufacturer part number', max_length=100),
        ),
        migrations.AddField(
            model_name='storagedevice',
            name='replaced_by',
            field=models.ForeignKey(blank=True, help_text='The storage device that replaced this one', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='replaced_devices', to='netbox_physical_storage.storagedevice'),
        ),
        migrations.AddField(
            model_name='storagedevice',
            name='status',
            field=models.CharField(choices=[('active', 'Active', 'green'), ('replaced', 'Replaced', 'orange'), ('removed', 'Removed', 'gray'), ('failed', 'Failed', 'red'), ('spare', 'Spare', 'blue')], default='active', help_text='Current status of the storage device', max_length=20),
        ),
        migrations.AlterField(
            model_name='storagedevice',
            name='serial_number',
            field=models.CharField(blank=True, help_text='Drive serial number (can be added later)', max_length=100),
        ),
        # Create RAIDGroup model
        migrations.CreateModel(
            name='RAIDGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('name', models.CharField(help_text='Name for this RAID group', max_length=100)),
                ('raid_level', models.CharField(choices=[('RAID0', 'RAID 0', 'red'), ('RAID1', 'RAID 1', 'green'), ('RAID2', 'RAID 2', 'yellow'), ('RAID3', 'RAID 3', 'yellow'), ('RAID4', 'RAID 4', 'yellow'), ('RAID5', 'RAID 5', 'blue'), ('RAID6', 'RAID 6', 'purple'), ('RAID10', 'RAID 10', 'cyan'), ('RAID01', 'RAID 01', 'orange'), ('RAID50', 'RAID 50', 'indigo'), ('RAID60', 'RAID 60', 'pink')], help_text='RAID level configuration', max_length=20)),
                ('description', models.TextField(blank=True, help_text='Optional description or configuration details')),
                ('device', models.ForeignKey(help_text='The enclosure device containing this RAID', on_delete=django.db.models.deletion.CASCADE, related_name='raid_groups', to='dcim.device')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'RAID Group',
                'verbose_name_plural': 'RAID Groups',
                'ordering': ('device', 'name'),
            },
        ),
        # Create StorageDeviceHistory model
        migrations.CreateModel(
            name='StorageDeviceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('status', models.CharField(choices=[('active', 'Active', 'green'), ('replaced', 'Replaced', 'orange'), ('removed', 'Removed', 'gray'), ('failed', 'Failed', 'red'), ('spare', 'Spare', 'blue')], help_text='Status at time of change', max_length=20)),
                ('replaced_at', models.DateTimeField(blank=True, help_text='When the replacement occurred', null=True)),
                ('notes', models.TextField(blank=True, help_text='Additional notes about this change')),
                ('bay', models.ForeignKey(blank=True, help_text='Bay the storage device was in at time of change', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='storage_device_history', to='netbox_physical_storage.storagebay')),
                ('device', models.ForeignKey(blank=True, help_text='Device the storage device was in at time of change', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='storage_device_history', to='dcim.device')),
                ('replaced_by', models.ForeignKey(blank=True, help_text='The storage device that replaced this one (if replaced)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='replacement_history', to='netbox_physical_storage.storagedevice')),
                ('storage_device', models.ForeignKey(help_text='The storage device being tracked', on_delete=django.db.models.deletion.CASCADE, related_name='history_records', to='netbox_physical_storage.storagedevice')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'Storage Device History',
                'verbose_name_plural': 'Storage Device History',
                'ordering': ('-replaced_at', '-created'),
            },
        ),
        # Add unique constraint for StorageBay
        migrations.AlterUniqueTogether(
            name='storagebay',
            unique_together={('device', 'bay_number')},
        ),
        # Add M2M relationship for RAIDGroup.storage_devices
        migrations.AddField(
            model_name='raidgroup',
            name='storage_devices',
            field=models.ManyToManyField(blank=True, help_text='Storage devices in this RAID group', related_name='raid_groups', to='netbox_physical_storage.storagedevice'),
        ),
        # Set default status for existing StorageDevices
        migrations.RunPython(
            code=lambda apps, schema_editor: apps.get_model('netbox_physical_storage', 'StorageDevice').objects.filter(status__isnull=True).update(status='active'),
            reverse_code=migrations.RunPython.noop,
        ),
    ]

