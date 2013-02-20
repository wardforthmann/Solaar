#
#
#

from __future__ import absolute_import, division, print_function, unicode_literals


NAME = 'Solaar'
from solaar import __version__

#
#
#

def _require(module, os_package):
	try:
		__import__(module)
	except ImportError:
		import sys
		sys.exit("%s: missing required package '%s'" % (NAME, os_package))


def _parse_arguments():
	import argparse
	arg_parser = argparse.ArgumentParser(prog=NAME.lower())
	arg_parser.add_argument('-N', '--no-notifications', action='store_false', dest='notifications',
							help='disable desktop notifications (shown only when in systray)')
	arg_parser.add_argument('-d', '--debug', action='count', default=0,
							help='print logging messages, for debugging purposes (may be repeated for extra verbosity)')
	arg_parser.add_argument('-V', '--version', action='version', version='%(prog)s ' + __version__)
	args = arg_parser.parse_args()

	import logging
	if args.debug > 0:
		log_level = logging.WARNING - 10 * args.debug
		log_format='%(asctime)s %(levelname)8s [%(threadName)s] %(name)s: %(message)s'
		logging.basicConfig(level=max(log_level, logging.DEBUG), format=log_format)
	else:
		logging.root.addHandler(logging.NullHandler())
		logging.root.setLevel(logging.CRITICAL)

	return args


def _run(args):
	import solaar.ui as ui

	# even if --no-notifications is given on the command line, still have to
	# check they are available, and decide whether to put the option in the
	# systray icon
	if ui.notify.init():
		ui.action.toggle_notifications.set_active(args.notifications)
		if not args.notifications:
			ui.notify.uninit()
	else:
		ui.action.toggle_notifications = None

	from solaar.listener import ReceiverListener
	window = ui.main_window.create(NAME, args.systray)
	assert window
	icon = ui.status_icon.create(window)
	assert icon

	listeners = {}
	from logitech.unifying_receiver import base as _base

	from gi.repository import Gtk, GLib
	from logitech.unifying_receiver import status

	def receivers_events(action, receiver):
		def _open_receiver(r):
			try:
				l = ReceiverListener.open(r.path, status_changed)
				if l:
					listeners[r.path] = l
			except OSError:
				# permission error, blacklist this path for now
				import logging
				logging.exception("failed to open %s", r.path)
				listeners[r.path] = None
				# ui.error_dialog(window, 'Permissions error',
				# 				'Found a possible Unifying Receiver device,\n'
				# 				'but did not have permission to open it.')

		if action == 'add':
			GLib.idle_add(_open_receiver, receiver)

	# callback delivering status notifications from the receiver/devices to the UI
	def status_changed(device, alert=status.ALERT.NONE, reason=None):
		assert device is not None
		# print ("status changed", device, reason)
		GLib.idle_add(ui.main_window.update, window, device)
		if alert & status.ALERT.WINDOW:
			GLib.idle_add(window.present)
			GLib.idle_add(ui.main_window.select, window, device)
		if icon:
			GLib.idle_add(ui.status_icon.update, icon, device)

		if ui.notify.available:
			# always notify on receiver updates
			if device.kind is None or alert & status.ALERT.NOTIFICATION:
				GLib.idle_add(ui.notify.show, device, reason)

	GLib.timeout_add(10, _base.notify_on_receivers, receivers_events)
	Gtk.main()

	[l.stop() for l in listeners.values() if l]
	ui.notify.uninit()
	[l.join() for l in listeners.values() if l]


def main():
	_require('pyudev', 'python-pyudev')
	_require('gi.repository', 'python-gi')
	_require('gi.repository.Gtk', 'gir1.2-gtk-3.0')
	args = _parse_arguments()

	from . import appinstance
	appid = appinstance.check()
	try:
		_run(args)
	finally:
		appinstance.close(appid)


if __name__ == '__main__':
	main()
