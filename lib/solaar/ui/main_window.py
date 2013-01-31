#
#
#

from __future__ import absolute_import, division, print_function, unicode_literals

from gi.repository import Gtk, Gdk, GObject, GLib

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

_TOOLTIP_LINK_SECURE = 'The wireless link between this device and its receiver is encrypted.'
_TOOLTIP_LINK_INSECURE = ('The wireless link between this device and its receiver is not encrypted.\n'
						'\n'
						'For pointing devices (mice, trackballs, trackpads), this is a minor security issue.\n'
						'\n'
						'It is, however, a major security issue for text-input devices (keyboards, numpads),\n'
						'because typed text can be sniffed inconspicuously by 3rd parties within range.')

#
#
#

def _find_selected_device(window):
	selection = window._tree.get_selection()
	model, it = selection.get_selected()
	return model.get_value(it, _COLUMN.OBJ) if it else None


def _device_selected(selection, window):
	model, it = selection.get_selected()
	device = model.get_value(it, _COLUMN.OBJ) if it else None
	# print ("selected", device)
	_update_info_panel(device, window, True)


def _receiver_row(tree, receiver, autocreate=True):
	model = tree.get_model()
	it = model.get_iter_first()
	while it:
		if model.get_value(it, _COLUMN.OBJ) == receiver:
			return it
		it = model.iter_next(it)

	if not it and autocreate:
		# print ("new receiver row", model.get_path(it), receiver, receiver.path, receiver.name)
		row_data = (receiver, True, receiver.name, _icons.device_icon_name(receiver.name), '')
		it = model.append(None, row_data)
	return it or None


def _device_row(tree, device, autocreate=True):
	receiver_row = _receiver_row(tree, device.receiver, autocreate)
	model = tree.get_model()
	it = model.iter_children(receiver_row)
	while it:
		if model.get_value(it, _COLUMN.OBJ) == device:
			return it
		it = model.iter_next(it)

	if not it and autocreate:
		# print ("new device row", device)
		row_data = (device, bool(device.status), device.codename, _icons.device_icon_name(device.name, device.kind), '')
		it = model.append(receiver_row, row_data)
	return it or None


def _show_details(button, window):
	visible = button.get_active()
	device = _find_selected_device(window)

	if visible:
		window._info._receiver.set_visible(False)
		window._info._device.set_visible(False)

		window._info._details._text.set_markup('<small>reading...</small>')
		window._info._details.set_visible(True)

		def _update_details_text(label, device):
			if device.kind is None:
				items = [('Path', device.path), ('Serial', device.serial)] + \
						[(fw.kind, fw.version) for fw in device.firmware]
			else:
				items = [None, None, None, None, None, None, None, None]
				hid = device.protocol
				items[0] = ('Protocol', 'HID++ %1.1f' % hid if hid else 'unknown')
				if device.polling_rate is not None:
					items[1] = ('Polling rate', '%d ms' % device.polling_rate)
				items[2] = ('Wireless PID', device.wpid)
				items[3] = ('Serial', device.serial)
				firmware = device.firmware
				if firmware:
					items[4:] = [(fw.kind, (fw.name + ' ' + fw.version).strip()) for fw in firmware]

			label.set_markup('<small><tt>%s</tt></small>' % '\n'.join('%-15s%s' % i for i in items if i))

		GLib.idle_add(_update_details_text, window._info._details._text, device)

	else:
		window._info._details.set_visible(False)
		_update_info_panel(device, window, True)


def select(window, device):
	it = _receiver_row(window._tree, device, False) if device.kind is None else _device_row(window._tree, device, False)
	if it:
		selection = window._tree.get_selection()
		selection.select_iter(it)

#
#
#

_UNIFYING_RECEIVER_TEXT = (
		'No paired devices.\n\n<small>Up to %d devices can be paired\nto this receiver.</small>',
		'%d paired device(s).\n\n<small>Up to %d devices can be paired\nto this receiver.</small>',
	)
_NANO_RECEIVER_TEXT = (
	'No paired device.\n\n<small> \n </small>',
	' \n\n<small>Only one device can be paired\nto this receiver.</small>',
	)

def _update_receiver_panel(receiver, info_panel, full=False):
	p = info_panel._receiver

	devices_count = len(receiver)
	if receiver.max_devices > 1:
		if devices_count == 0:
			p._count.set_markup(_UNIFYING_RECEIVER_TEXT[0] % receiver.max_devices)
		else:
			p._count.set_markup(_UNIFYING_RECEIVER_TEXT[1] % (devices_count, receiver.max_devices))
	else:
		if devices_count == 0:
			p._count.set_text(_NANO_RECEIVER_TEXT[0])
		else:
			p._count.set_markup(_NANO_RECEIVER_TEXT[1])

	if receiver.status.lock_open:
		p._scanning.set_visible(True)
		if not p._spinner.get_visible():
			p._spinner.start()
		p._spinner.set_visible(True)
	else:
		p._scanning.set_visible(False)
		if p._spinner.get_visible():
			p._spinner.stop()
		p._spinner.set_visible(False)

	b = info_panel._buttons
	# b._insecure.set_visible(False)
	b._unpair.set_visible(False)
	b._pair.set_sensitive(devices_count < receiver.max_devices and not receiver.status.lock_open)
	b._pair.set_visible(True)


def _update_device_panel(device, info_panel, full=False):
	active = bool(device.status)
	p = info_panel._device
	p.set_sensitive(active)

	battery_level = device.status.get(_status.BATTERY_LEVEL)
	if battery_level is None:
		p._battery._icon.set_sensitive(False)
		p._battery._icon.set_from_icon_name(_icons.battery(-1), Gtk.IconSize.LARGE_TOOLBAR)
		p._battery._text.set_sensitive(True)
		p._battery._text.set_markup('<small>unknown</small>')
	else:
		p._battery._icon.set_from_icon_name(_icons.battery(battery_level), Gtk.IconSize.LARGE_TOOLBAR)
		p._battery._icon.set_sensitive(True)
		p._battery._text.set_text('%d%%' % battery_level)
		p._battery._text.set_sensitive(True)

	if active:
		not_secure = device.status.get(_status.ENCRYPTED) == False
		if not_secure:
			p._secure._text.set_text('not encrypted')
			p._secure._icon.set_from_icon_name('security-low', Gtk.IconSize.LARGE_TOOLBAR)
			p._secure.set_tooltip_text(_TOOLTIP_LINK_INSECURE)
		else:
			p._secure._text.set_text('encrypted')
			p._secure._icon.set_from_icon_name('security-high', Gtk.IconSize.LARGE_TOOLBAR)
			p._secure.set_tooltip_text(_TOOLTIP_LINK_SECURE)
		p._secure._icon.set_visible(True)
	else:
		p._secure._text.set_markup('<small>not connected</small>')
		p._secure._icon.set_visible(False)
		p._secure.set_tooltip_text('')

	if active:
		light_level = device.status.get(_status.LIGHT_LEVEL)
		if light_level is None:
			p._lux.set_visible(False)
		else:
			p._lux._icon.set_from_icon_name(_icons.lux(light_level), Gtk.IconSize.LARGE_TOOLBAR)
			p._lux._text.set_text('%d lux' % light_level)
			p._lux.set_visible(True)
	else:
		p._lux.set_visible(False)

	GLib.idle_add(_config_panel.update, p._config, device, active)

	b = info_panel._buttons
	b._pair.set_visible(False)
	b._unpair.set_visible(True)


def _update_info_panel(device, window, full=False):
	if device is None:
		window._info.set_visible(False)
		window._empty.set_visible(True)
		return

	p = window._info
	active = bool(device.status)

	p._title.set_markup('<b>%s</b>' % device.name)
	p._title.set_sensitive(active)
	p._icon.set_from_icon_name(_icons.device_icon_name(device.name, device.kind), Gtk.IconSize.DND)
	p._icon.set_sensitive(active)

	if p._details.get_visible():
		if full:
			p._buttons._details.set_active(False)
		else:
			_show_details(p._buttons._details, window)
			return

	p._details.set_visible(False)
	if device.kind is None:
		p._device.set_visible(False)
		_update_receiver_panel(device, p, full)
		p._receiver.set_visible(True)
	else:
		p._receiver.set_visible(False)
		_update_device_panel(device, p, full)
		p._device.set_visible(True)

	window._empty.set_visible(False)
	p.set_visible(True)


def update(window, receiver, device=None):
	assert receiver is not None
	# print ("update", receiver, receiver, len(receiver), device)
	# window.set_icon_name(_icons.APP_ICON[1 if receiver else -1])

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
	selected_device = _find_selected_device(window)
	if device == selected_device:
		_update_info_panel(device, window)
	elif selected_device is None:
		select(window, device)

#
# create UI layout
#

def _new_button(label, icon_name=None, icon_size=Gtk.IconSize.BUTTON, tooltip=None, toggle=False):
	if toggle:
		b = Gtk.ToggleButton()
	else:
		b = Gtk.Button(label) if label else Gtk.Button()

	if icon_name:
		image = Gtk.Image.new_from_icon_name(icon_name, icon_size)
		b.set_image(image)

	if tooltip:
		b.set_tooltip_text(tooltip)

	if not label and icon_size < Gtk.IconSize.BUTTON:
		b.set_relief(Gtk.ReliefStyle.NONE)
		b.set_focus_on_click(False)

	return b


def _create_receiver_panel():
	p = Gtk.Box.new(Gtk.Orientation.VERTICAL, 4)

	p._count = Gtk.Label()
	p._count.set_padding(32, 0)
	p._count.set_alignment(0, 0.5)
	p.pack_start(p._count, True, True, 0)

	p._scanning = Gtk.Label('Scanning...')
	p._spinner = Gtk.Spinner()

	bp = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 8)
	bp.pack_start(Gtk.Label(' '), True, True, 0)
	bp.pack_start(p._scanning, False, False, 0)
	bp.pack_end(p._spinner, False, False, 0)
	p.pack_end(bp, False, False, 0)
	return p


def _create_device_panel():
	p = Gtk.Box.new(Gtk.Orientation.VERTICAL, 4)

	def _status_line(label_text):
		b = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 8)
		b.set_size_request(10, 28)

		b._label = Gtk.Label(label_text)
		b._label.set_alignment(0, 0.5)
		b._label.set_size_request(170, 10)
		b.pack_start(b._label, False, False, 0)

		b._icon = Gtk.Image()
		b.pack_start(b._icon, False, False, 0)

		b._text = Gtk.Label()
		b._text.set_alignment(0, 0.5)
		b.pack_start(b._text, True, True, 0)

		return b

	p._battery = _status_line('Battery')
	p.pack_start(p._battery, False, False, 0)

	p._lux = _status_line('Lighting')
	p.pack_start(p._lux, False, False, 0)

	p._secure = _status_line('Wireless Link')
	p._secure._icon.set_from_icon_name('dialog-warning', Gtk.IconSize.LARGE_TOOLBAR)
	p.pack_start(p._secure, False, False, 0)

	p._config = _config_panel.create()
	p.pack_end(p._config, False, False, 8)

	return p


def _create_details_panel(window):
	p = Gtk.Frame()
	p.set_border_width(32)
	p.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)

	p._text = Gtk.Label()
	p._text.set_alignment(0.5, 0.5)
	p._text.set_selectable(True)
	p.add(p._text)

	return p


def _create_buttons_box(window):
	bb = Gtk.ButtonBox(Gtk.Orientation.HORIZONTAL)
	bb.set_layout(Gtk.ButtonBoxStyle.END)

	bb._details = _new_button(None, 'dialog-information', Gtk.IconSize.SMALL_TOOLBAR, 'Show Details', True)
	bb._details.connect('clicked', _show_details, window)
	bb.add(bb._details)
	bb.set_child_secondary(bb._details, True)
	bb.set_child_non_homogeneous(bb._details, True)

	bb._pair = _new_button('Pair new device', 'list-add')
	bb.add(bb._pair)

	bb._unpair = _new_button('Unpair', 'edit-delete')
	bb.add(bb._unpair)

	return bb


def _create_info_panel(window):
	panel = Gtk.Box.new(Gtk.Orientation.VERTICAL, 4)

	panel._title = Gtk.Label(' ')
	panel._title.set_alignment(0, 0.5)
	panel._icon = Gtk.Image()

	b1 = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 4)
	b1.pack_start(panel._title, True, True, 0)
	b1.pack_start(panel._icon, False, False, 0)
	panel.pack_start(b1, False, False, 0)

	panel.pack_start(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL), False, False, 0)  # spacer

	panel._details = _create_details_panel(window)
	panel.pack_start(panel._details, True, True, 0)

	panel._receiver = _create_receiver_panel()
	panel.pack_start(panel._receiver, True, True, 0)

	panel._device = _create_device_panel()
	panel.pack_start(panel._device, True, True, 0)

	panel.pack_start(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL), False, False, 0)  # spacer

	panel._buttons = _create_buttons_box(window)
	panel.pack_end(panel._buttons, False, False, 0)

	panel.show_all()
	panel._details.set_visible(False)
	panel._receiver.set_visible(False)
	panel._device.set_visible(False)
	panel._buttons._pair.set_visible(False)
	panel._buttons._unpair.set_visible(False)
	return panel


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
	window._tree = _create_tree()
	assert window._tree.get_selection().get_mode() == Gtk.SelectionMode.SINGLE
	window._tree.get_selection().connect('changed', _device_selected, window)

	window._info = _create_info_panel(window)

	window._empty = Gtk.Label()
	window._empty.set_markup('<small>Select a device</small>')
	window._empty.set_sensitive(False)

	panel = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 16)
	panel.pack_start(window._tree, False, False, 0)
	panel.pack_start(window._info, True, True, 0)
	panel.pack_start(window._empty, True, True, 0)

	about_button = Gtk.Button('About')
	about_button.set_image(Gtk.Image.new_from_icon_name('help-about', Gtk.IconSize.BUTTON))
	about_button.connect('clicked', _action._show_about_window)
	about_button.set_relief(Gtk.ReliefStyle.NONE)

	bottom_buttons_box = Gtk.ButtonBox(Gtk.Orientation.HORIZONTAL)
	bottom_buttons_box.set_layout(Gtk.ButtonBoxStyle.START)
	bottom_buttons_box.add(about_button)

	vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 8)
	vbox.set_border_width(8)
	vbox.pack_start(panel, True, True, 0)
	vbox.pack_end(bottom_buttons_box, False, False, 0)
	vbox.show_all()

	window._info.set_visible(False)

	window.add(vbox)
	return vbox


def create(title, name, max_devices, systray=False):
	window = Gtk.Window()
	window.set_title(title)
	window.set_icon_name(_icons.APP_ICON[1])
	window.set_role('status-window')

	_create_window_layout(window)

	geometry = Gdk.Geometry()
	geometry.min_width = 600
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
