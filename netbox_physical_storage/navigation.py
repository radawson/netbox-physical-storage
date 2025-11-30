"""
Define the plugin menu buttons & the plugin navigation bar enteries.
"""

from django.conf import settings
from netbox.plugins.navigation import PluginMenu, PluginMenuButton, PluginMenuItem
from netbox.choices import ButtonColorChoices

plugin_settings = settings.PLUGINS_CONFIG.get("netbox_physical_storage", {})

#
# Define storage device menu buttons
#
storagedevice_buttons = [
    PluginMenuButton(
        link='plugins:netbox_physical_storage:storagedevice_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN,
    )
]

#
# Define storage bay menu buttons
#
storagebay_buttons = [
    PluginMenuButton(
        link='plugins:netbox_physical_storage:storagebay_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN,
    )
]

#
# Define RAID group menu buttons
#
raidgroup_buttons = [
    PluginMenuButton(
        link='plugins:netbox_physical_storage:raidgroup_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN,
    )
]

#
# Define the top-level menu
#
menu_buttons = (
    PluginMenuItem(
        link='plugins:netbox_physical_storage:storagedevice_list',
        link_text='Storage Devices',
        buttons=storagedevice_buttons,
    ),
    PluginMenuItem(
        link='plugins:netbox_physical_storage:storagebay_list',
        link_text='Storage Bays',
        buttons=storagebay_buttons,
    ),
    PluginMenuItem(
        link='plugins:netbox_physical_storage:raidgroup_list',
        link_text='RAID Groups',
        buttons=raidgroup_buttons,
    ),
    PluginMenuItem(
        link='plugins:netbox_physical_storage:storagedevicehistory_list',
        link_text='History',
    ),
)

if plugin_settings.get("top_level_menu", True):
    menu = PluginMenu(
        label="Physical Storage",
        groups=(
            ("Storage", (
                PluginMenuItem(
                    link='plugins:netbox_physical_storage:storagedevice_list',
                    link_text='Storage Devices',
                    buttons=storagedevice_buttons,
                ),
                PluginMenuItem(
                    link='plugins:netbox_physical_storage:storagebay_list',
                    link_text='Storage Bays',
                    buttons=storagebay_buttons,
                ),
            )),
            ("RAID", (
                PluginMenuItem(
                    link='plugins:netbox_physical_storage:raidgroup_list',
                    link_text='RAID Groups',
                    buttons=raidgroup_buttons,
                ),
            )),
            ("History", (
                PluginMenuItem(
                    link='plugins:netbox_physical_storage:storagedevicehistory_list',
                    link_text='Device History',
                ),
            )),
        ),
        icon_class="mdi mdi-harddisk",
    )
else:
    menu_items = menu_buttons