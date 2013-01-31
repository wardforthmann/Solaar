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
	arg_parser.add_argument('-S', '--no-systray', action='store_false', dest='systray',
							help='do not place an icon in the desktop\'s systray')
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
	args.notifications &= args.systray
	if args.systray and ui.notify.init(NAME):
		ui.action.toggle_notifications.set_active(args.notifications)
		if not args.notifications:
			ui.notify.uninit()
	else:
		ui.action.toggle_notifications = None

	from solaar.listener import DUMMY, ReceiverListener
	window = ui.main_window.create(NAME, DUMMY.name, DUMMY.max_devices, args.systray)
	if args.systray:
		menu_actions = (ui.action.toggle_notifications,
						ui.action.about)
		icon = ui.status_icon.create(window, menu_actions)
	else:
		icon = None

	listeners = {}
	from logitech.unifying_receiver import base as _base

	def receivers_events(action, r):
		if action == 'add':
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

	from gi.repository import Gtk, GLib
	from logitech.unifying_receiver import status

	# callback delivering status notifications from the receiver/devices to the UI
	def status_changed(receiver, device=None, alert=status.ALERT.NONE, reason=None):
		# print ("status changed", receiver, device, reason)
		if alert & status.ALERT.MED:
			GLib.idle_add(window.present)
		if window:
			GLib.idle_add(ui.main_window.update, window, receiver, device)
			if device and alert & status.ALERT.MED:
				GLib.idle_add(ui.main_window.select, window, device)
		if icon:
			GLib.idle_add(ui.status_icon.update, icon, receiver, device)

		if ui.notify.available:
			# always notify on receiver updates
			if device is None or alert & status.ALERT.LOW:
				GLib.idle_add(ui.notify.show, device or receiver, reason)

	GLib.timeout_add(10, _base.notify_on_receivers, receivers_events)
	Gtk.main()

	[l.stop() for l in listeners.values() if l]
	ui.notify.uninit()


def main():
	_require('pyudev', 'python-pyudev')
	_require('gi.repository', 'python-gi')
	_require('gi.repository.Gtk', 'gir1.2-gtk-3.0')
	args = _parse_arguments()

	# ensure no more than a single instance runs at a time
	import os.path as _path
	import os as _os
	lock_fd = None
	for p in _os.environ.get('XDG_RUNTIME_DIR'), '/run/lock', '/var/lock', _os.environ.get('TMPDIR', '/tmp'):
		if p and _path.isdir(p) and _os.access(p, _os.W_OK):
			lock_path = _path.join(p, 'solaar.single-instance.%d' % _os.getuid())
			try:
				lock_fd = open(lock_path, 'wb')
				# print ("Single instance lock file is %s" % lock_path)
				break
			except:
				pass

	if lock_fd:
		import fcntl as _fcntl
		try:
			_fcntl.flock(lock_fd, _fcntl.LOCK_EX | _fcntl.LOCK_NB)
		except IOError as e:
			if e.errno == 11:
				import sys
				sys.exit("solaar: error: Solaar is already running.")
			else:
				raise
	else:
		import sys
		print ("solaar: warning: failed to create single instance lock file, ignoring.", file=sys.stderr)

	try:
		_run(args)
	finally:
		if lock_fd:
			_fcntl.flock(lock_fd, _fcntl.LOCK_UN)
			lock_fd.close()

if __name__ == '__main__':
	main()
