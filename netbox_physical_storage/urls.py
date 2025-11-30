from netbox.views.generic import ObjectChangeLogView
from django.urls import path
from . import models, views

urlpatterns = (
    # StorageDevice URLs
    path('physical-storage/', views.StorageDeviceListView.as_view(), name='storagedevice_list'),
    path('physical-storage/add/', views.StorageDeviceEditView.as_view(), name='storagedevice_add'),
    path('physical-storage/<int:pk>/', views.StorageDeviceView.as_view(), name='storagedevice'),
    path('physical-storage/<int:pk>/edit/', views.StorageDeviceEditView.as_view(), name='storagedevice_edit'),
    path('physical-storage/<int:pk>/delete/', views.StorageDeviceDeleteView.as_view(), name='storagedevice_delete'),
    path('physical-storage/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='storagedevice_changelog', kwargs={
        'model': models.StorageDevice
    }),
    # StorageBay URLs
    path('storage-bays/', views.StorageBayListView.as_view(), name='storagebay_list'),
    path('storage-bays/add/', views.StorageBayEditView.as_view(), name='storagebay_add'),
    path('storage-bays/<int:pk>/', views.StorageBayView.as_view(), name='storagebay'),
    path('storage-bays/<int:pk>/edit/', views.StorageBayEditView.as_view(), name='storagebay_edit'),
    path('storage-bays/<int:pk>/delete/', views.StorageBayDeleteView.as_view(), name='storagebay_delete'),
    path('storage-bays/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='storagebay_changelog', kwargs={
        'model': models.StorageBay
    }),
    # RAIDGroup URLs
    path('raid-groups/', views.RAIDGroupListView.as_view(), name='raidgroup_list'),
    path('raid-groups/add/', views.RAIDGroupEditView.as_view(), name='raidgroup_add'),
    path('raid-groups/<int:pk>/', views.RAIDGroupView.as_view(), name='raidgroup'),
    path('raid-groups/<int:pk>/edit/', views.RAIDGroupEditView.as_view(), name='raidgroup_edit'),
    path('raid-groups/<int:pk>/delete/', views.RAIDGroupDeleteView.as_view(), name='raidgroup_delete'),
    path('raid-groups/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='raidgroup_changelog', kwargs={
        'model': models.RAIDGroup
    }),
    # StorageDeviceHistory URLs
    path('storage-device-history/', views.StorageDeviceHistoryListView.as_view(), name='storagedevicehistory_list'),
    path('storage-device-history/<int:pk>/', views.StorageDeviceHistoryView.as_view(), name='storagedevicehistory'),
    path('storage-device-history/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='storagedevicehistory_changelog', kwargs={
        'model': models.StorageDeviceHistory
    }),
)