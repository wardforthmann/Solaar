#
#
#

from __future__ import absolute_import, division, print_function, unicode_literals

#
#
#

try:
	from gi.repository import AppIndicator3 as AppIndicator
except:
	from gi.repository import AppIndicator

from gi.repository import Gtk

from . import (action as _action,
				notify as _notify,
				icons as _icons,
				main_window as _main_window)
# from logitech.unifying_receiver import status as _status


def create(window):
	name = window.get_title()

	ind = AppIndicator.Indicator.new('indicator-solaar', _icons.APP_ICON[0], AppIndicator.IndicatorCategory.HARDWARE)
	ind.set_title(name)
	ind._window = window

	menu = Gtk.Menu()
	ind.set_menu(menu)

	no_devices = Gtk.MenuItem.new_with_label('No devices')
	no_devices.set_sensitive(False)
	menu.append(no_devices)

	separator = Gtk.SeparatorMenuItem.new()
	separator.set_name('')
	menu.append(separator)

	menu.append(_action.make_toggle('notifications', 'Notifications', _notify.toggle))
	menu.append(_action.make('application-exit', 'Quit', Gtk.main_quit))
	menu.show_all()

	ind.set_status(AppIndicator.IndicatorStatus.ACTIVE)
	return ind


def destroy(ind):
	ind.set_status(AppIndicator.IndicatorStatus.PASSIVE)
	ind.set_menu(None)


def _create_menu_item(ind, device):
	item = Gtk.MenuItem.new()
	item.set_name(device.serial)
	item.set_visible(True)
	item.connect('activate', _main_window.select, ind._window, device)
	_update_menu_item(item, device)
	return item


def _update_menu_item(item, device):
	if device.status is None:
		item.get_parent().remove(item)
		return

	item.set_label(device.name)


def update(ind, device):
	assert device is not None
	if device.kind is None:
		return

	# print (device, device.status)

	m = ind.get_menu()
	items = m.get_children()
	index = 1
	while True:
		n = items[index].get_name()
		if n:
			if n == device.serial:
				_update_menu_item(items[index], device)
				break
		else:
			if device.status is not None:
				m.insert(_create_menu_item(ind, device), index)
			break

		index += 1

	items[0].set_visible(index == 1 and not m.get_children()[1].get_name())
