from netbox.views import generic
from . import filtersets, forms, models, tables

# StorageDevice Views
class StorageDeviceView(generic.ObjectView):
    queryset = models.StorageDevice.objects.all()
    
class StorageDeviceListView(generic.ObjectListView):
    queryset = models.StorageDevice.objects.all()
    table = tables.StorageDeviceTable
    filterset = filtersets.StorageDeviceFilterSet
    filterset_form = forms.StorageDeviceFilterForm

class StorageDeviceEditView(generic.ObjectEditView):
    queryset = models.StorageDevice.objects.all()
    form = forms.StorageDeviceForm

class StorageDeviceDeleteView(generic.ObjectDeleteView):
    queryset = models.StorageDevice.objects.all()

# StorageBay Views
class StorageBayView(generic.ObjectView):
    queryset = models.StorageBay.objects.all()

class StorageBayListView(generic.ObjectListView):
    queryset = models.StorageBay.objects.all()
    table = tables.StorageBayTable
    filterset = filtersets.StorageBayFilterSet
    filterset_form = forms.StorageBayFilterForm

class StorageBayEditView(generic.ObjectEditView):
    queryset = models.StorageBay.objects.all()
    form = forms.StorageBayForm

class StorageBayDeleteView(generic.ObjectDeleteView):
    queryset = models.StorageBay.objects.all()

# RAIDGroup Views
class RAIDGroupView(generic.ObjectView):
    queryset = models.RAIDGroup.objects.all()

class RAIDGroupListView(generic.ObjectListView):
    queryset = models.RAIDGroup.objects.all()
    table = tables.RAIDGroupTable
    filterset = filtersets.RAIDGroupFilterSet
    filterset_form = forms.RAIDGroupFilterForm

class RAIDGroupEditView(generic.ObjectEditView):
    queryset = models.RAIDGroup.objects.all()
    form = forms.RAIDGroupForm

class RAIDGroupDeleteView(generic.ObjectDeleteView):
    queryset = models.RAIDGroup.objects.all()

# StorageDeviceHistory Views
class StorageDeviceHistoryView(generic.ObjectView):
    queryset = models.StorageDeviceHistory.objects.all()

class StorageDeviceHistoryListView(generic.ObjectListView):
    queryset = models.StorageDeviceHistory.objects.all()
    table = tables.StorageDeviceHistoryTable
    filterset = filtersets.StorageDeviceHistoryFilterSet
    filterset_form = forms.StorageDeviceHistoryFilterForm