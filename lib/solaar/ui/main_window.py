#
#
#

from __future__ import absolute_import, division, print_function, unicode_literals

from gi.repository import Gtk, Gdk, GObject

from logitech.unifying_receiver import status as _status
from logitech.unifying_receiver.common import NamedInts as _NamedInts
from . import config_panel as _config_panel
from . import action as _action, icons as _icons

#
#
#

_RECEIVER_ICON_SIZE = Gtk.IconSize.LARGE_TOOLBAR
_DEVICE_ICON_SIZE = Gtk.IconSize.DIALOG
_STATUS_ICON_SIZE = Gtk.IconSize.LARGE_TOOLBAR
_TOOLBAR_ICON_SIZE = Gtk.IconSize.MENU
_PLACEHOLDER = '~'
_FALLBACK_ICON = 'preferences-desktop-peripherals'

# tree model columns
_COLUMN = _NamedInts(OBJ=0, ACTIVE=1, NAME=2, ICON=3, STATUS_ICON=4)
_COLUMN_TYPES = (GObject.TYPE_PYOBJECT, bool, str, str, str)

#
#
#

# def _make_receiver_box(name):
# 	frame = Gtk.Frame()
# 	frame._device = None
# 	frame.set_name(name)

# 	icon_set = _icons.device_icon_set(name)
# 	icon = Gtk.Image.new_from_icon_set(icon_set, _RECEIVER_ICON_SIZE)
# 	icon.set_padding(2, 2)
# 	frame._icon = icon

# 	label = Gtk.Label('Scanning...')
# 	label.set_alignment(0, 0.5)
# 	frame._label = label

# 	pairing_icon = Gtk.Image.new_from_icon_name('network-wireless', _RECEIVER_ICON_SIZE)
# 	pairing_icon.set_tooltip_text('The pairing lock is open.')
# 	pairing_icon._tick = 0
# 	frame._pairing_icon = pairing_icon

# 	toolbar = Gtk.Toolbar()
# 	toolbar.set_style(Gtk.ToolbarStyle.ICONS)
# 	toolbar.set_icon_size(_TOOLBAR_ICON_SIZE)
# 	toolbar.set_show_arrow(False)
# 	frame._toolbar = toolbar

# 	hbox = Gtk.HBox(homogeneous=False, spacing=8)
# 	hbox.pack_start(icon, False, False, 0)
# 	hbox.pack_start(label, True, True, 0)
# 	hbox.pack_start(pairing_icon, False, False, 0)
# 	hbox.pack_start(toolbar, False, False, 0)

# 	info_label = Gtk.Label()
# 	info_label.set_markup('<small>reading ...</small>')
# 	info_label.set_property('margin-left', 36)
# 	info_label.set_alignment(0, 0)
# 	info_label.set_selectable(True)
# 	frame._info_label = info_label

# 	def _update_info_label(f):
# 		device = f._device
# 		if f._info_label.get_visible() and '\n' not in f._info_label.get_text():
# 			items = [('Path', device.path), ('Serial', device.serial)] + \
# 					[(fw.kind, fw.version) for fw in device.firmware]
# 			f._info_label.set_markup('<small><tt>%s</tt></small>' % '\n'.join('%-13s: %s' % item for item in items))

# 	def _toggle_info_label(action, f):
# 		active = action.get_active()
# 		vb = f.get_child()
# 		for c in vb.get_children()[1:]:
# 			c.set_visible(active)

# 		if active:
# 			GObject.timeout_add(50, _update_info_label, f)

# 	toggle_info_action = _action.make_toggle('dialog-information', 'Details', _toggle_info_label, frame)
# 	toolbar.insert(toggle_info_action.create_tool_item(), 0)
# 	toolbar.insert(_action.pair(frame).create_tool_item(), -1)
# 	# toolbar.insert(ui.action.about.create_tool_item(), -1)

# 	vbox = Gtk.VBox(homogeneous=False, spacing=2)
# 	vbox.set_border_width(2)
# 	vbox.pack_start(hbox, True, True, 0)
# 	vbox.pack_start(Gtk.HSeparator(), False, False, 0)
# 	vbox.pack_start(info_label, True, True, 0)

# 	frame.add(vbox)
# 	frame.show_all()

# 	pairing_icon.set_visible(False)
# 	_toggle_info_label(toggle_info_action, frame)
# 	return frame


# def _make_device_box(index):
# 	frame = Gtk.Frame()
# 	frame._device = None
# 	frame.set_name(_PLACEHOLDER)

# 	icon = Gtk.Image.new_from_icon_name(_FALLBACK_ICON, _DEVICE_ICON_SIZE)
# 	icon.set_alignment(0.5, 0)
# 	frame._icon = icon

# 	label = Gtk.Label('Initializing...')
# 	label.set_alignment(0, 0.5)
# 	label.set_padding(4, 0)
# 	frame._label = label

# 	battery_icon = Gtk.Image.new_from_icon_name(_icons.battery(-1), _STATUS_ICON_SIZE)

# 	battery_label = Gtk.Label()
# 	battery_label.set_width_chars(6)
# 	battery_label.set_alignment(0, 0.5)

# 	light_icon = Gtk.Image.new_from_icon_name('light_unknown', _STATUS_ICON_SIZE)

# 	light_label = Gtk.Label()
# 	light_label.set_alignment(0, 0.5)
# 	light_label.set_width_chars(8)

# 	not_encrypted_icon = Gtk.Image.new_from_icon_name('security-low', _STATUS_ICON_SIZE)
# 	not_encrypted_icon.set_name('not-encrypted')
# 	not_encrypted_icon.set_tooltip_text('The wireless link between this device and the Unifying Receiver is not encrypted.\n'
# 										'\n'
# 										'For pointing devices (mice, trackballs, trackpads), this is a minor security issue.\n'
# 										'\n'
# 										'It is, however, a major security issue for text-input devices (keyboards, numpads),\n'
# 										'because typed text can be sniffed inconspicuously by 3rd parties within range.')

# 	toolbar = Gtk.Toolbar()
# 	toolbar.set_style(Gtk.ToolbarStyle.ICONS)
# 	toolbar.set_icon_size(_TOOLBAR_ICON_SIZE)
# 	toolbar.set_show_arrow(False)
# 	frame._toolbar = toolbar

# 	status_box = Gtk.HBox(homogeneous=False, spacing=2)
# 	status_box.pack_start(battery_icon, False, True, 0)
# 	status_box.pack_start(battery_label, False, True, 0)
# 	status_box.pack_start(light_icon, False, True, 0)
# 	status_box.pack_start(light_label, False, True, 0)
# 	status_box.pack_end(toolbar, False, False, 0)
# 	status_box.pack_end(not_encrypted_icon, False, False, 0)
# 	frame._status_icons = status_box

# 	status_vbox = Gtk.VBox(homogeneous=False, spacing=4)
# 	status_vbox.pack_start(label, True, True, 0)
# 	status_vbox.pack_start(status_box, True, True, 0)

# 	device_box = Gtk.HBox(homogeneous=False, spacing=4)
# 	# device_box.set_border_width(4)
# 	device_box.pack_start(icon, False, False, 0)
# 	device_box.pack_start(status_vbox, True, True, 0)
# 	device_box.show_all()

# 	info_label = Gtk.Label()
# 	info_label.set_markup('<small>reading ...</small>')
# 	info_label.set_property('margin-left', 54)
# 	info_label.set_selectable(True)
# 	info_label.set_alignment(0, 0)
# 	frame._info_label = info_label

# 	def _update_info_label(f):
# 		if frame._info_label.get_text().count('\n') < 4:
# 			device = f._device
# 			assert device

# 			items = [None, None, None, None, None, None, None, None]
# 			hid = device.protocol
# 			items[0] = ('Protocol', 'HID++ %1.1f' % hid if hid else 'unknown')
# 			items[1] = ('Polling rate', '%d ms' % device.polling_rate)
# 			items[2] = ('Wireless PID', device.wpid)
# 			items[3] = ('Serial', device.serial)
# 			firmware = device.firmware
# 			if firmware:
# 				items[4:] = [(fw.kind, (fw.name + ' ' + fw.version).strip()) for fw in firmware]

# 			frame._info_label.set_markup('<small><tt>%s</tt></small>' % '\n'.join('%-13s: %s' % i for i in items if i))

# 	def _toggle_info_label(action, f):
# 		active = action.get_active()
# 		if active:
# 			# set config toggle button as inactive
# 			f._toolbar.get_children()[-1].set_active(False)

# 		vb = f.get_child()
# 		children = vb.get_children()
# 		children[1].set_visible(active)  # separator
# 		children[2].set_visible(active)  # info label

# 		if active:
# 			GObject.timeout_add(30, _update_info_label, f)

# 	def _toggle_config(action, f):
# 		active = action.get_active()
# 		if active:
# 			# set info toggle button as inactive
# 			f._toolbar.get_children()[0].set_active(False)

# 		vb = f.get_child()
# 		children = vb.get_children()
# 		children[1].set_visible(active)  # separator
# 		children[3].set_visible(active)  # config box
# 		children[4].set_visible(active)  # unpair button

# 		if active:
# 			GObject.timeout_add(30, _config_panel.update, f)

# 	toggle_info_action = _action.make_toggle('dialog-information', 'Details', _toggle_info_label, frame)
# 	toolbar.insert(toggle_info_action.create_tool_item(), 0)
# 	toggle_config_action = _action.make_toggle('preferences-system', 'Configuration', _toggle_config, frame)
# 	toolbar.insert(toggle_config_action.create_tool_item(), -1)

# 	vbox = Gtk.VBox(homogeneous=False, spacing=2)
# 	vbox.set_border_width(2)
# 	vbox.pack_start(device_box, True, True, 0)
# 	vbox.pack_start(Gtk.HSeparator(), False, False, 0)
# 	vbox.pack_start(info_label, False, False, 0)

# 	frame._config_box = _config_panel.create()
# 	vbox.pack_start(frame._config_box, False, False, 0)

# 	unpair = Gtk.Button('Unpair')
# 	unpair.set_image(Gtk.Image.new_from_icon_name('edit-delete', Gtk.IconSize.BUTTON))
# 	unpair.connect('clicked', _action._unpair_device, frame)
# 	unpair.set_relief(Gtk.ReliefStyle.NONE)
# 	unpair.set_property('margin-left', 106)
# 	unpair.set_property('margin-right', 106)
# 	unpair.set_property('can-focus', False)  # exclude from tab-navigation
# 	vbox.pack_end(unpair, False, False, 0)

# 	vbox.show_all()
# 	frame.add(vbox)

# 	_toggle_info_label(toggle_info_action, frame)
# 	_toggle_config(toggle_config_action, frame)
# 	return frame


def _update_info_panel(device, info_panel):
	if device is None:
		info_panel._not_accessible.set_visible(False)
		info_panel._receiver_info.set_visible(False)
		info_panel._device_info.set_visible(False)
		info_panel._no_selection.set_visible(True)
		return

	if device.kind is None:
		p = info_panel._receiver_info

		# receiver
		p._icon.set_from_icon_name(_icons.device_icon_name(device.name), Gtk.IconSize.DIALOG)
		p._title.set_text(device.name)

		devices_count = len(device)
		if device.max_devices > 1:
			p._start_pairing_button.set_visible(True)
			if devices_count:
				p._count.set_text('%d paired device(s).' % devices_count)
			else:
				p._count.set_text('No devices paired.')
			p._max_count.set_markup('<small>This receiver supports 6 paired devices.</small>')
		else:
			if devices_count:
				p._count.set_text('')
				p._start_pairing_button.set_visible(False)
			else:
				p._count.set_text('No device paired.')
				p._start_pairing_button.set_visible(True)
			p._max_count.set_markup('<small>Only one device can be paired to this receiver.</small>')

		if device.status.lock_open:
			p._start_pairing_button.set_visible(False)
			p._stop_pairing_button.set_visible(True)
			# p._pairing_text.set_visible(True)
			# p._pairing_icon.set_visible(True)
		else:
			p._start_pairing_button.set_visible(devices_count < device.max_devices)
			p._stop_pairing_button.set_visible(False)
			# p._pairing_text.set_visible(False)
			# p._pairing_icon.set_visible(False)

		info_panel._no_selection.set_visible(False)
		info_panel._not_accessible.set_visible(False)
		info_panel._device_info.set_visible(False)
		info_panel._receiver_info.set_visible(True)
		return

	# regular device
	info_panel._no_selection.set_visible(False)
	info_panel._not_accessible.set_visible(False)
	info_panel._receiver_info.set_visible(False)
	info_panel._device_info.set_visible(True)


def _device_selected(selection, info_panel):
	model, iter = selection.get_selected()
	device = model.get_value(iter, _COLUMN.OBJ) if iter else None
	print ("selected", device, model.get_path(iter) if iter else None)
	_update_info_panel(device, info_panel)

#
# create UI layout
#

def _create_info_panel():
	info_panel = Gtk.VBox(homogeneous=False, spacing=4)
	info_panel.set_border_width(4)
	# info_panel.set_size_request(400, 200)

	no_selection = Gtk.Label()
	no_selection.set_markup('<small>Select a device</small>')
	no_selection.set_sensitive(False)
	info_panel.pack_start(no_selection, True, True, 0)
	info_panel._no_selection = no_selection

	not_accessible = Gtk.VBox(homogeneous=False, spacing=4)
	info_panel.pack_start(not_accessible, True, True, 0)
	info_panel._not_accessible = not_accessible

	def _create_device_info():
		panel = Gtk.VBox(homogeneous=False, spacing=4)
		return panel

	info_panel._device_info = _create_device_info()
	info_panel.pack_start(info_panel._device_info, True, True, 0)

	def _create_receiver_info():
		panel = Gtk.VBox(homogeneous=False, spacing=4)

		panel._title = Gtk.Label()
		panel._title.set_alignment(1, 0.5)
		panel._icon = Gtk.Image()

		b1 = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 4)
		b1.pack_start(panel._title, True, True, 0)
		b1.pack_start(panel._icon, False, False, 0)
		panel.pack_start(b1, False, False, 0)

		panel._count = Gtk.Label()
		panel._count.set_alignment(0, 1)
		panel.pack_start(panel._count, True, True, 0)

		panel._max_count = Gtk.Label()
		panel._max_count.set_alignment(0, 0)
		panel.pack_start(panel._max_count, False, False, 0)

		panel._pairing_text = Gtk.Label('The pairing lock is open.')
		panel._pairing_icon = Gtk.Image.new_from_icon_name('network-wireless', Gtk.IconSize.BUTTON)
		b2 = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 4)
		b2.pack_start(panel._pairing_text, False, False, 0)
		b2.pack_start(panel._pairing_icon, False, False, 0)
		b2.pack_start(Gtk.Label(), True, True, 0)
		panel.pack_start(b2, True, True, 0)

		buttons_box = Gtk.ButtonBox(Gtk.Orientation.HORIZONTAL)
		buttons_box.set_layout(Gtk.ButtonBoxStyle.END)
		panel._start_pairing_button = Gtk.Button('Pair new device')
		panel._stop_pairing_button = Gtk.Button('Stop pairing')
		panel._info_button = Gtk.Button('Info')
		buttons_box.add(panel._start_pairing_button)
		buttons_box.add(panel._stop_pairing_button)
		buttons_box.add(panel._info_button)
		buttons_box.set_child_secondary(panel._info_button, True)

		panel.pack_end(buttons_box, False, False, 0)

		return panel

	info_panel._receiver_info = _create_receiver_info()
	info_panel.pack_start(info_panel._receiver_info, True, True, 0)

	info_panel.show_all()
	info_panel._not_accessible.set_visible(False)
	info_panel._receiver_info.set_visible(False)
	info_panel._device_info.set_visible(False)
	return info_panel


def _create_tree():
	tree = Gtk.TreeView()
	tree.set_size_request(220, 100)
	tree.set_headers_visible(False)
	tree.set_show_expanders(False)
	tree.set_level_indentation(16)
	tree.set_enable_tree_lines(True)
	tree.set_model(Gtk.TreeStore(*_COLUMN_TYPES))

	icon_cell_renderer = Gtk.CellRendererPixbuf()
	icon_cell_renderer.set_property('stock-size', Gtk.IconSize.LARGE_TOOLBAR)
	icon_column = Gtk.TreeViewColumn('Icon', icon_cell_renderer)
	icon_column.add_attribute(icon_cell_renderer, 'sensitive', _COLUMN.ACTIVE)
	icon_column.add_attribute(icon_cell_renderer, 'icon-name', _COLUMN.ICON)
	icon_column.set_fixed_width(1)
	tree.append_column(icon_column)

	name_cell_renderer = Gtk.CellRendererText()
	name_column = Gtk.TreeViewColumn('Name', name_cell_renderer)
	name_column.add_attribute(name_cell_renderer, 'sensitive', _COLUMN.ACTIVE)
	name_column.add_attribute(name_cell_renderer, 'text', _COLUMN.NAME)
	name_column.set_expand(True)
	tree.append_column(name_column)
	tree.set_expander_column(name_column)

	battery_cell_renderer = Gtk.CellRendererPixbuf()
	battery_cell_renderer.set_property('stock-size', Gtk.IconSize.LARGE_TOOLBAR)
	battery_column = Gtk.TreeViewColumn('Status', battery_cell_renderer)
	battery_column.add_attribute(battery_cell_renderer, 'sensitive', _COLUMN.ACTIVE)
	battery_column.add_attribute(battery_cell_renderer, 'icon-name', _COLUMN.STATUS_ICON)
	battery_column.set_fixed_width(1)
	tree.append_column(battery_column)

	return tree


def _create_window_layout(window):
	window._info = _create_info_panel()
	window._tree = _create_tree()
	assert window._tree.get_selection().get_mode() == Gtk.SelectionMode.SINGLE
	window._tree.get_selection().connect('changed', _device_selected, window._info)

	panel = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 4)
	panel.pack_start(window._tree, False, False, 0)
	panel.pack_start(window._info, True, True, 0)

	about_button = Gtk.Button('About')
	about_button.set_image(Gtk.Image.new_from_icon_name('help-about', Gtk.IconSize.BUTTON))
	about_button.connect('clicked', _action._show_about_window)
	about_button.set_relief(Gtk.ReliefStyle.NONE)

	bottom_buttons_box = Gtk.ButtonBox(Gtk.Orientation.HORIZONTAL)
	bottom_buttons_box.set_layout(Gtk.ButtonBoxStyle.START)
	bottom_buttons_box.add(about_button)

	vbox = Gtk.VBox(homogeneous=False, spacing=8)
	vbox.set_border_width(8)
	vbox.pack_start(panel, True, True, 0)
	vbox.pack_end(bottom_buttons_box, False, False, 0)
	vbox.show_all()
	window.add(vbox)
	return vbox


def create(title, name, max_devices, systray=False):
	window = Gtk.Window()
	window.set_title(title)
	window.set_icon_name(_icons.APP_ICON[1])
	window.set_role('status-window')

	_create_window_layout(window)

	geometry = Gdk.Geometry()
	geometry.min_width = 540
	geometry.min_height = 320
	window.set_geometry_hints(window.get_child(), geometry, Gdk.WindowHints.MIN_SIZE)

	def _toggle_visible(w, trigger):
		if w.get_visible():
			# hiding moves the window to 0,0
			position = w.get_position()
			w.hide()
			w.move(*position)
		else:
			if isinstance(trigger, Gtk.StatusIcon):
				x, y = w.get_position()
				if x == 0 and y == 0:
					# if the window hasn't been shown yet, position it next to the status icon
					x, y, _ = Gtk.StatusIcon.position_menu(Gtk.Menu(), trigger)
					w.move(x, y)
			w.present()
		return True

	def _set_has_systray(w, systray):
		if systray != w._has_systray:
			w._has_systray = systray
			if systray:
				if w._delete_event_connection is None or not w.get_skip_taskbar_hint():
					w.set_skip_taskbar_hint(True)
					w.set_skip_pager_hint(True)
					if w._delete_event_connection:
						w.disconnect(w._delete_event_connection)
					w._delete_event_connection = w.connect('delete-event', _toggle_visible)
			else:
				if w._delete_event_connection is None or w.get_skip_taskbar_hint():
					w.set_skip_taskbar_hint(False)
					w.set_skip_pager_hint(False)
					if w._delete_event_connection:
						w.disconnect(w._delete_event_connection)
					w._delete_event_connection = w.connect('delete-event', Gtk.main_quit)
					w.present()

	from types import MethodType
	window.toggle_visible = MethodType(_toggle_visible, window)
	window.set_has_systray = MethodType(_set_has_systray, window)
	del MethodType

	window.set_keep_above(True)
	window._delete_event_connection = None
	window._has_systray = None
	window.set_has_systray(systray)

	return window

#
#
#

# def _update_receiver_box(frame, receiver):
# 	frame._label.set_text(str(receiver.status))
# 	if receiver:
# 		frame._device = receiver
# 		frame._icon.set_sensitive(True)
# 		if receiver.status.lock_open:
# 			if frame._pairing_icon._tick == 0:
# 				def _pairing_tick(i, s):
# 					if s and s.lock_open:
# 						i.set_sensitive(bool(i._tick % 2))
# 						i._tick += 1
# 						return True
# 					i.set_visible(False)
# 					i.set_sensitive(True)
# 					i._tick = 0
# 				frame._pairing_icon.set_visible(True)
# 				GObject.timeout_add(1000, _pairing_tick, frame._pairing_icon, receiver.status)
# 		else:
# 			frame._pairing_icon.set_visible(False)
# 			frame._pairing_icon.set_sensitive(True)
# 			frame._pairing_icon._tick = 0
# 		frame._toolbar.set_sensitive(True)
# 	else:
# 		frame._device = None
# 		frame._icon.set_sensitive(False)
# 		frame._pairing_icon.set_visible(False)
# 		frame._toolbar.set_sensitive(False)
# 		frame._toolbar.get_children()[0].set_active(False)
# 		frame._info_label.set_text('')


# def _update_device_box(frame, dev):
# 	if dev is None:
# 		frame.set_visible(False)
# 		frame.set_name(_PLACEHOLDER)
# 		frame._device = None
# 		_config_panel.update(frame)
# 		return

# 	first_run = frame.get_name() != dev.name
# 	if first_run:
# 		frame._device = dev
# 		frame.set_name(dev.name)
# 		icon_set = _icons.device_icon_set(dev.name, dev.kind)
# 		frame._icon.set_from_icon_set(icon_set, _DEVICE_ICON_SIZE)
# 		frame._label.set_markup('<b>%s</b>' % dev.name)
# 		for i in frame._toolbar.get_children():
# 			i.set_active(False)

# 	battery_icon, battery_label, light_icon, light_label, not_encrypted_icon, _ = frame._status_icons
# 	battery_level = dev.status.get(_status.BATTERY_LEVEL)

# 	if dev.status:
# 		frame._label.set_sensitive(True)

# 		if battery_level is None:
# 			battery_icon.set_sensitive(False)
# 			battery_icon.set_from_icon_name(_icons.battery(-1), _STATUS_ICON_SIZE)
# 			battery_label.set_markup('<small>no status</small>')
# 			battery_label.set_sensitive(True)
# 		else:
# 			battery_icon.set_from_icon_name(_icons.battery(battery_level), _STATUS_ICON_SIZE)
# 			battery_icon.set_sensitive(True)
# 			battery_label.set_text('%d%%' % battery_level)
# 			battery_label.set_sensitive(True)

# 		battery_status = dev.status.get(_status.BATTERY_STATUS)
# 		battery_icon.set_tooltip_text(battery_status or '')

# 		light_level = dev.status.get(_status.LIGHT_LEVEL)
# 		if light_level is None:
# 			light_icon.set_visible(False)
# 			light_label.set_visible(False)
# 		else:
# 			icon_name = 'light_%03d' % (20 * ((light_level + 50) // 100))
# 			light_icon.set_from_icon_name(icon_name, _STATUS_ICON_SIZE)
# 			light_icon.set_visible(True)
# 			light_label.set_text('%d lux' % light_level)
# 			light_label.set_visible(True)

# 		not_encrypted_icon.set_visible(dev.status.get(_status.ENCRYPTED) == False)

# 	else:
# 		frame._label.set_sensitive(False)

# 		battery_icon.set_sensitive(False)
# 		battery_label.set_sensitive(False)
# 		if battery_level is None:
# 			battery_label.set_markup('<small>inactive</small>')
# 		else:
# 			battery_label.set_markup('%d%%' % battery_level)

# 		light_icon.set_visible(False)
# 		light_label.set_visible(False)
# 		not_encrypted_icon.set_visible(False)

# 		frame._toolbar.get_children()[-1].set_active(False)

# 	frame.set_visible(True)
# 	_config_panel.update(frame)


def update(window, receiver, device=None):
	assert receiver is not None
	# print ("update", receiver, receiver, len(receiver), device)
	# window.set_icon_name(_icons.APP_ICON[1 if receiver else -1])

	def _receiver_row(tree, receiver, autocreate=True):
		model = tree.get_model()
		iter = model.get_iter_first()
		while iter:
			if model.get_value(iter, _COLUMN.OBJ) == receiver:
				return iter
			iter = model.iter_next(iter)
		if not iter and autocreate:
			# print ("new receiver row", model.get_path(iter), receiver, receiver.path, receiver.name)
			row_data = (receiver, True, receiver.name, _icons.device_icon_name(receiver.name), '')
			iter = model.append(None, row_data)
		return iter or None

	def _device_row(tree, device, autocreate=True):
		receiver_row = _receiver_row(tree, device.receiver, autocreate)
		model = tree.get_model()
		iter = model.iter_children(receiver_row)
		while iter:
			if model.get_value(iter, _COLUMN.OBJ) == device:
				return iter
			iter = model.iter_next(iter)
		if not iter and autocreate:
			# print ("new device row", device)
			row_data = (device, bool(device.status), device.codename, _icons.device_icon_name(device.name, device.kind), '')
			iter = model.append(receiver_row, row_data)
		return iter or None

	model = window._tree.get_model()
	if device is None:
		iter = _receiver_row(window._tree, receiver, bool(receiver))
		assert iter
		if receiver:
			model.set_value(iter, _COLUMN.ACTIVE, True)
		elif iter:
			model.remove(iter)

	else:
		iter = _device_row(window._tree, device)
		assert iter
		model.set_value(iter, _COLUMN.ACTIVE, bool(device.status))
		battery_level = device.status.get(_status.BATTERY_LEVEL)
		battery_icon_name = _icons.battery(-1 if battery_level is None else battery_level)
		model.set_value(iter, _COLUMN.STATUS_ICON, '' if battery_level is None else battery_icon_name)

	window._tree.expand_all()
	_device_selected(window._tree.get_selection(), window._info)
