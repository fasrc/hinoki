#! /usr/bin/env python3

'''

sensu 2.0 api calls

requires python3
- validate json for asset definitions and check defintions
- sync asset and check definitions to API
- sync actual asset files to server

'''

import json
import requests
from urllib import parse
from hinoki.logger import log
from hinoki.config import config

class SensuAPICall:
	
	headers={'Content-Type': 'application/json', 'Accept': 'application/json'}
	token=""
	last_resp_content={}

	def test_get(self, endpoint):
		try:
			endpoint=config['api_items']['check']["endpoint"]
		except KeyError as e:
			return False
		result=self.perform_api_call(endpoint=endpoint, method="GET")

	def sync_definition(self, item_type, file):
		try:
			directory=config['api_items'][item_type]["dir"]
			endpoint=config['api_items'][item_type]["endpoint"]
		except KeyError as e:
			log.error("Couldn't find an entry for these parameters in the project configuration")
			log.debug("Item type passed to function: "+item_type)
			log.debug("Filename passed to function: "+file)
			log.debug(e)
			return False
		fh=open(directory+"/"+file, 'r')
		try:
		  item=json.load(fh)
		except (json.decoder.JSONDecodeError, UnicodeDecodeError):
			message='Error importing definition for file '+file+': invalid JSON.'
			log.error(message)
			return False
		name="/"+file.split('.json')[0]
		result=self.perform_api_call(endpoint+name, request_body=json.dumps(item))
		fh.close()
		return result

	# accepts a user and password, both required
	# sets the auth token, or False and logs errors
	def api_auth(self, user=config['api_user'], password=config['api_password'], auth_endpoint=config['api_auth_endpoint']):
		resp=requests.get(auth_endpoint, auth=(user, password), headers=self.headers)
		try:
			data=json.loads(resp.content.decode('utf-8'))
		except ValueError:
			log.error("Unable to log in.")
		try:
			token=data['access_token']
		except NameError:
			log.error("Unable to authenticate to API, no token retrieved.")
			return False
		self.token=token
		return True

	def test_connection(self):
		try:
			health=requests.get(config['api_healthcheck_endpoint'], timeout=10)
		except requests.exceptions.ConnectionError:
			log.error('Could not reach API health check')
			return False
		try:
			health.raise_for_status()
		except requests.exceptions.ConnectionError:
			log.error('Could not reach API health check - network or DNS error')
			return False
		except requests.exceptions.HTTPError:
			log.error('Could not reach API health check - HTTP error %s' % str(health.status_code))
			log.debug('Response headers: %s' % json.dumps(dict(health.headers)))
			return False
		log.info('API health check completed successfully.')
		log.debug('Status code: %s' % health.status_code)
		return True

	def perform_api_call(self, endpoint, method="PUT", request_body={}):
		auth_header={'Authorization': self.token}
		auth_header.update(self.headers)
		request_url = parse.urljoin(config['api_url'], endpoint)
		log.debug(request_url)
		resp=requests.request(method, request_url, headers=auth_header, data=request_body)
		try:
			resp.raise_for_status()
		except requests.exceptions.HTTPError:
			log.error('Error '+str(resp.status_code))
			log.debug('Request URL: '+request_url)
			log.debug('Response headers: %s' % json.dumps(dict(resp.headers)))
			log.error(str.resp.text)
			return False
		#og.debug(resp.content)
		self.last_resp_content=resp.content.decode('utf8')
		return True

sensu_connect = SensuAPICall()
