# Local Installation Guide (For Testing)

## Quick Install

### Method 1: Editable Install (Recommended for Development)

```bash
# Activate your NetBox Python environment
# For netbox-docker, this might be:
# docker-compose exec netbox bash
# source /opt/netbox/venv/bin/activate

# Navigate to plugin directory
cd /home/torvaldsl/netbox-physical-storage

# Install in editable mode
pip install -e .
```

### Method 2: Direct Install

```bash
# From your NetBox environment
pip install /home/torvaldsl/netbox-physical-storage
```

### Method 3: Using Requirements File (netbox-docker)

Add to your `plugin_requirements.txt`:

```
-e /home/torvaldsl/netbox-physical-storage
```

Then rebuild:
```bash
docker-compose build netbox
docker-compose up -d
```

## Configuration

1. **Enable the plugin** in NetBox configuration:

   For netbox-docker: `/configuration/plugins.py`
   For direct install: `/opt/netbox/netbox/netbox/configuration.py`

   ```python
   PLUGINS = [
       "netbox_physical_storage"
   ]

   PLUGINS_CONFIG = {
       "netbox_physical_storage": {
           "top_level_menu": True
       },
   }
   ```

2. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Restart NetBox**:
   ```bash
   # netbox-docker
   docker-compose restart netbox
   
   # Direct install
   sudo systemctl restart netbox
   ```

## Verify Installation

1. Check plugin is loaded:
   ```bash
   python manage.py shell
   >>> from extras.plugins import get_plugin_config
   >>> get_plugin_config('netbox_physical_storage', 'version')
   ```

2. Access the plugin in NetBox UI:
   - Look for "Physical Storage" in the navigation menu
   - Or go to Plugins > Physical Storage

## Troubleshooting

- **Plugin not showing**: Check that it's in `PLUGINS` list and NetBox was restarted
- **Import errors**: Verify you're using the correct Python environment
- **Migration errors**: Make sure all dependencies are installed (`netbox>=4.0.0,<4.5.0`)

