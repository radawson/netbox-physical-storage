# Changelog

These are notes from the early development versions.

## v0.1.0 - Device, Bay, and RAID Support - R. Dawson

* [FEATURE] Add StorageBay model to track physical bay/slot locations within enclosures
* [FEATURE] Add RAIDGroup model with support for all standard RAID levels (0, 1, 2, 3, 4, 5, 6, 10, 01, 50, 60)
* [FEATURE] Add RAID capacity calculation utilities for all RAID levels
* [FEATURE] Add RAID failure tolerance calculation (how many drives can fail before data loss)
* [FEATURE] Add StorageDeviceHistory model for tracking drive replacements and lifecycle changes
* [FEATURE] Link StorageDevice to NetBox Device (enclosures like Dell MD1400/MD1200)
* [FEATURE] Add status tracking to StorageDevice (Active, Replaced, Removed, Failed, Spare)
* [FEATURE] Add replacement tracking with replaced_by ForeignKey
* [FEATURE] Add model_number, manufacturer, and capacity_gb fields to StorageDevice
* [FEATURE] Support incomplete data entry (all new fields are nullable/optional)
* [FEATURE] Add complete CRUD views for StorageBay, RAIDGroup, and StorageDeviceHistory
* [FEATURE] Add API endpoints for all new models with computed fields
* [FEATURE] Add search indexes for all new models
* [FEATURE] Add GraphQL support for all new models
* [FEATURE] Update navigation menu with Storage Bays, RAID Groups, and History sections
* [COMPATIBILITY] Update imports for NetBox 4.4.7 compatibility:
  * `extras.plugins` → `netbox.plugins`
  * `netbox.filters` → `utilities.filters`
  * `extras.plugins` (navigation) → `netbox.plugins.navigation`
  * `utilities.choices` (ButtonColorChoices) → `netbox.choices`
* [COMPATIBILITY] Update minimum NetBox version to 4.0.0
* [COMPATIBILITY] Update forms to use DynamicModelChoiceField with queryset parameter
* [COMPATIBILITY] Update filter forms to use DynamicModelMultipleChoiceField
* [COMPATIBILITY] Fix urlpatterns to use list format instead of tuple

## v0.0.2 - Backwards Forwards

* [BREAKING] Removes the "Mount point" option for now
* [bugfix] Fix display of serial numbers in the main StorageDevice view

## v0.0.1 - The First Drop

* Basic functionality
* Can set the following:

  * Name
  * Type of storage device (SAS, SATA, NVMe)
  * Serial number
  * Mount point
