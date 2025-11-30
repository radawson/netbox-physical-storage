from netbox.plugins import PluginConfig

class NetBoxPhysicalStorageConfig(PluginConfig):
    name = 'netbox_physical_storage'
    verbose_name = ' NetBox Physical Storage'
    description = 'Manage physical storage interfaces and devices in NetBox.'
    version = '0.1.0'
    author = 'R. Dawson'
    author_email = 'dawsonra@clockworx.org'  
    base_url = 'physical-storage'
    min_version = '4.0.0'
    max_version = '4.4.99'

config = NetBoxPhysicalStorageConfig