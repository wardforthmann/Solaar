#
#
#

import os as _os
import os.path as _path
from json import load as _json_load, dump as _json_save

import logging

_XDG_CONFIG_HOME = _os.environ.get('XDG_CONFIG_HOME') or _path.join(_path.expanduser('~'), '.config')
file_path = _path.join(_path.join(_XDG_CONFIG_HOME, 'solaar'), 'config.json')


from solaar import __version__
_configuration = {}


def _load():
	if _path.isfile(file_path):
		loaded_configuration = {}
		try:
			with open(file_path, 'r') as config_file:
				loaded_configuration = _json_load(config_file)
		except:
			logging.error("failed to load configuration from %s", file_path)

		# loaded_configuration.update(_configuration)
		_configuration.clear()
		_configuration.update(loaded_configuration)

	_configuration['_Solaar'] = __version__
	return _configuration


def save():
	dirname = _os.path.dirname(file_path)
	if not _path.isdir(dirname):
		try:
			_os.makedirs(dirname)
		except:
			logging.error("failed to create %s", dirname)
			return False

	try:
		with open(file_path, 'w') as config_file:
			_json_save(_configuration, config_file, skipkeys=True, indent=2, sort_keys=True)
		return True
	except:
		logging.error("failed to save to configuration file %s", file_path)


def all():
	if not _configuration:
		_load()

	return dict(_configuration)


def _device_key(device):
	return '%s:%s' % (device.serial, device.kind)

def _device_entry(device):
	if not _configuration:
		_load()

	device_key = _device_key(device)
	if device_key in _configuration:
		c = _configuration[device_key]
	else:
		c = _configuration[device_key] = {}

	c['_name'] = device.name
	return c


def set(device, key, value):
	_device_entry(device)[key] = value


def get(device, key, default_value=None):
	return _device_entry(device).get(key, default_value)


def sync(device):
	if not _configuration:
		_load()

	entry = _device_entry(device)
	for s in device.settings:
		value = s.read()
		if s.name in entry:
			if value is None:
				del entry[s.name]
			elif value != entry[s.name]:
				s.write(entry[s.name])
		else:
			entry[s.name] = value


def forget(device):
	if not _configuration:
		_load()

	device_key = _device_key(device)
	if device_key in _configuration:
		del _configuration[device_key]
