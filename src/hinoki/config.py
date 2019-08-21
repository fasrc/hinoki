import os
import sys
import yaml

def load_config():

    config = {}

    # maybe make the default behavior to use the data directory, then make the 

    # runtime/repo vars
    config['config_file_dir'] = os.path.join(os.path.expanduser('~'), '.hinoki')
    config['config_file_path'] = os.path.join(config['config_file_dir'], 'config.yml')
    config['main_script_dir'] = os.path.dirname(os.path.realpath(sys.argv[0]))
    # vars stored in config file
    # this ensures that anything specified in the config file overwrites what's specified here
    try:
        configfile = open(config['config_file_path'], 'r')
    except OSError:
        print('Error attempting to open config file '+config['config_file_path']+' for reading.')
        return False
    configvals = yaml.load(configfile, Loader=yaml.Loader)
    configfile.close()

    config.update(configvals)

    # dictinoary describing API structure and endpoints
    try:
        config['api_items'] = {
            "asset": {
                "endpoint": "namespaces/default/assets",
                "dir": os.path.join(config['definition_base_dir'], 'asset-definitions')
            },
            "check": {
                "endpoint": "namespaces/default/checks",
                "dir": os.path.join(config['definition_base_dir'], 'check-definitions')
            },
            "user": {
                "endpoint": "users"
            },
            "filter": {
                "endpoint": "namespaces/default/filters",
                "dir": os.path.join(config['definition_base_dir'], 'filter-definitions')
            },
            "handler": {
                "endpoint": "namespaces/default/handlers",
                "dir": os.path.join(config['definition_base_dir'], 'handler-definitions')
            }
        }
    except KeyError:
        return False

    config['asset_files_dir'] = os.path.join(config['definition_base_dir'], 'asset-files')
    config['check_scripts_dir'] = os.path.join(config['definition_base_dir'], 'check-scripts')
    config['check_defs_dir'] = os.path.join(config['definition_base_dir'], 'check-definitions')
    config['asset_defs_dir'] = os.path.join(config['definition_base_dir'], 'asset-definitions')
    config['filter_defs_dir'] = os.path.join(config['definition_base_dir'], 'filter-definitions')
    config['handler_defs_dir'] = os.path.join(config['definition_base_dir'], 'handler-definitions')

    try:
        config['api_url']=config['api_version_endpoint']
    except KeyError:
        print('KeyError attempting to set api_url')
        return False

    try:
        config['syslog_handler']
    except KeyError:
        config['syslog_handler'] = '/dev/log'

    try:
        config['log_level']
    except KeyError:
        config['log_level'] = 'INFO'

    return config

config = load_config()
if config == False:
    print("Error creating config, exiting.")
    exit(1)
