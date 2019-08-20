#! /usr/bin/python3

'''
 
 init script to do some tasks we want after initializing a new cluster

'''

import json
from hinoki.logger import log
from hinoki.sensuapi import sensu_connect
from hinoki.config import config

def init_cluster():
  log.info("Connecting to API with default credentials....")
  api_user_role_name="api-user"
  api_user_role_binding_name="api-user-grant"
  cluster_role_endpoint="clusterroles/"+api_user_role_name
  role_binding_endpoint="clusterrolebindings/"+api_user_role_name

  sensu_connect.api_auth(user=config['default_admin_user'], password=config['default_admin_password'])

  create_api_user_body=json.dumps(
  {
    "username": config['api_user'],
    "password": config['api_password']
  })

  log.info("Creating API user....")
  sensu_connect.perform_api_call(endpoint=config['api_items']['user']['endpoint']+"/"+config['api_user'], request_body=create_api_user_body)

  create_role_body=json.dumps(
  {
      "metadata": {
        "name":"api-user",
        "namepsace": "*"
      },
      "rules": [
        {
          "verbs": [
            "get","list","create","update","delete"
          ],
          "resources": [
            "assets","checks","entities","events","filters","handlers","hooks","mutators","silenced"
          ],
        }
      ]
  })

  log.debug(create_role_body)
  log.info("Creating API role....")
  sensu_connect.perform_api_call(endpoint=cluster_role_endpoint, request_body=create_role_body)

  create_role_binding_body=json.dumps(
  {
      "metadata": {
        "name": api_user_role_binding_name,
      },
      "role_ref": {
        "type": "ClusterRole",
        "name": api_user_role_name
      },
      "subjects": [ 
          {
            "type": "User",
            "name": config['api_user']
          }
      ]
  })

  log.debug(create_role_binding_body)
  log.info("Creating API role binding....")
  sensu_connect.perform_api_call(endpoint=role_binding_endpoint, request_body=create_role_binding_body)
  change_pwd_body=json.dumps(
  {
    "username": config['default_admin_user'],
    "password": config['secure_admin_password'],
    "groups": [
      "cluster-admins"
    ]
  })

  log.info("Updating default password...")
  sensu_connect.perform_api_call(endpoint=config['api_items']['user']['endpoint']+"/"+config['default_admin_user'], request_body=change_pwd_body)

  log.info("Setup complete!")