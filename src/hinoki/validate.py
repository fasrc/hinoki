#! /usr/bin/python3

# todo: validate that ttl is greater than check interval

import json
import os
from hinoki.config import config
from hinoki.logger import log

###

## should be able to pass in a config['api_object'] obj instead of all of this stuff:
## def validate_names(config_obj):
##    for file in os.listdir(config_obj['dir']):
def validate_names(dir_to_validate, object_type):
	obj_names=[]
	for file in os.listdir(dir_to_validate):
		log.debug(file)
		try:
			contents=json.load(open(os.path.join(dir_to_validate,file)))
		except (json.decoder.JSONDecodeError, ValueError):
			log.info("Directory contains a file with invalid JSON: "+os.path.join(dir_to_validate,file))
			return False
		filename=os.path.splitext(file)[0]
		try:
			objname=contents["metadata"]["name"]
		except KeyError:
			log.error("A name for the check must be specified inside the 'metadata' block of the configuration file.")
			return False
		if filename != objname:
			log.error("The filename of the definition json is required to match the 'name' attribute within the definition.")
			return False
		obj_names.append(objname)
		if obj_names.count(objname) > 1:
			log.error("There is more than one check with the same name.  Failing check: "+objname)
			return False
		if object_type == "check":
			try:
				if (contents["ttl"] <= contents["interval"]):
					log.error("The ttl must be greater than the check interval")
					return False
			except (KeyError, ValueError):
				pass

	log.info("All "+object_type+" tests passed successfully.")
	return True

def main():
	validation_message={
		'checks': validate_names(config['check_defs_dir'], "check"),
		'assets': validate_names(config['asset_defs_dir'], "asset"),
		'filters': validate_names(config['filter_defs_dir'], "filter"),
		'handlers': validate_names(config['handler_defs_dir'], "handler")
	}

	# can use config['api_items'] for name and messaging, as in import_definitions.py
	# for item_name, item_obj in config['api_items']:

	for k,v in validation_message.items():
		if not v:
			log.info("Failed validation at %s stage.", k)
			exit(1)
	# if not (checks_result and assets_result and filters_result and handlers_result):
	# 	log.info("Validation failed!")

	# 	exit(1)
	log.info("All tests passed!")
	exit(0)

if __name__ == "__main__":
	main()