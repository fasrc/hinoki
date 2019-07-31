import json
from hinoki.sensuapi import sensu_connect
from hinoki.config import config

# TODO: switch so this can be used to change the password from what's in the config to something new.

sensu_connect.api_auth(user=config['default_admin_user'], password=config['default_admin_password'])

change_pwd_body=json.dumps(
 {
   "username": config['default_admin_user'],
   "password": config['secure_admin_password'],
   "groups": [
    "cluster-admins"
  ]
 })

sensu_connect.perform_api_call(endpoint=config['api_items']['user']['endpoint']+"/"+config['default_admin_user'], request_body=change_pwd_body)

'''
Equivalent operation using sensuctl on the command line is best done in interactive mode

sensuctl user change-password admin --interactive

'''