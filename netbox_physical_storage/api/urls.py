from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'netbox_physical_storage'

router = NetBoxRouter()
router.register('storage-devices', views.StorageDeviceViewSet)
router.register('storage-bays', views.StorageBayViewSet)
router.register('raid-groups', views.RAIDGroupViewSet)
router.register('storage-device-history', views.StorageDeviceHistoryViewSet)

urlpatterns = router.urls