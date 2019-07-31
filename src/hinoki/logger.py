"""
Logger for sensu sync module
"""

import logging
from logging import handlers
from hinoki.config import config

def log_setup():
    log = logging.getLogger('sensu-checks-logger')
    log.setLevel(config['log_level'])
    syslog_handler = logging.handlers.SysLogHandler(config['syslog_handler'])
    cli_handler = logging.StreamHandler()
    syslog_handler.setLevel(config['log_level'])
    cli_handler.setLevel(config['log_level'])
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    syslog_handler.setFormatter(formatter)
    log.addHandler(syslog_handler)
    log.addHandler(cli_handler)
    return log

log = log_setup()