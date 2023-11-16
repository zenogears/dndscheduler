import sys
import gi

from gettext import gettext as _

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio

from .helper import main_func, job_status, set_status, ALLDAYS, ret_days

def timecreators(timech):
    return(''.join([str(0), str(timech)]) if len(timech) < 2 else timech)

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        cfg = main_func()
        super().__init__(*args, **kwargs)
        self.set_default_size(360, 720)
        self.set_title("DND Scheduler")

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.box.set_margin_top(20)
        self.box.set_margin_start(10)
        self.box.set_margin_end(10)
        self.set_child(self.box)

        self.switch_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)


        self.label_from = Gtk.Label(label=_("Do not disturb from:"))
        self.button_from = Gtk.Button(label=f"{timecreators(cfg['main']['SHOUR'])}:{timecreators(cfg['main']['SMIN'])}")

        self.label_to = Gtk.Label(label=_("Do not disturb to:"))
        self.button_to = Gtk.Button(label=f"{timecreators(cfg['main']['EHOUR'])}:{timecreators(cfg['main']['EMIN'])}")

        self.label_repeat = Gtk.Label(label=_("Repeat:"))
        self.button_repeat = Gtk.Button(label=f"{ret_days()}")

        self.button_about = Gtk.Button(label=_("About application"))

        self.label_onoff = Gtk.Label(label=f"{_('Start params:')} {job_status('ENABLED')['text']}")
        self.switch_onoff = Gtk.Switch()
        self.switch_onoff.set_active(job_status("ENABLED")["status"])
        self.switch_onoff.connect("state-set", self.switch_switched, "ENABLED")
        self.switch_box.append(self.switch_onoff)

        self.box.append(self.label_from)
        self.box.append(self.button_from)

        self.box.append(self.label_to)
        self.box.append(self.button_to)

        self.box.append(self.label_repeat)
        self.box.append(self.button_repeat)

        self.box.append(self.label_onoff)
        self.box.append(self.switch_box)

        self.box.append(self.button_about)

        self.button_from.connect('clicked', self.bfrom)
        self.button_to.connect('clicked', self.bto)
        self.button_repeat.connect('clicked', self.brepeat)
        self.button_about.connect('clicked', self.show_about)

    def brepeat(self, brepeat):
        self.brepeat_form = Gtk.ApplicationWindow(transient_for=app.get_active_window())
        self.brepeat_form.set_default_size(360, 720)
        self.brepeat_form.set_title(_("Repeat on days:"))
        self.brepeat_form.show()

        self.box_repeat = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.box_repeat.set_margin_top(20)
        self.box_repeat.set_margin_start(10)
        self.box_repeat.set_margin_end(10)
        self.brepeat_form.set_child(self.box_repeat)

        for day in ALLDAYS:
            self.box_day = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            self.label_day = Gtk.Label(label=f"{ALLDAYS[day]}:", halign=Gtk.Align.START)
            self.label_day.set_hexpand(True)
            self.switch_day = Gtk.Switch(halign=Gtk.Align.CENTER)
            self.switch_day.set_active(job_status(day)["status"])
            self.switch_day.connect("state-set", self.switch_func, day)
            self.box_day.append(self.label_day)
            self.box_day.append(self.switch_day)
            self.box_repeat.append(self.box_day)

        self.button_repeat_close = Gtk.Button.new_with_mnemonic(_("SAVE"))
        self.button_repeat_close.connect("clicked", self.on_close_clicked, self.brepeat_form)
        self.box_repeat.append(self.button_repeat_close)

    def switch_func(self, switch, state, param):
        set_status(param, state)
        self.button_repeat.set_label(ret_days())

    def bfrom(self, bfrom):
        cfg = main_func()
        self.before_form = Gtk.ApplicationWindow(transient_for=app.get_active_window())
        self.before_form.set_default_size(360, 720)
        self.before_form.set_title(_("Start time"))
        self.before_form.show()

        self.box_from = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        self.before_form.set_child(self.box_from)
        self.label_from = Gtk.Label(label = _('Select hours:'))
        self.label_from_min = Gtk.Label(label = _('Select minutes:'))

        self.hour_store = Gtk.ListStore(str)
        time = [x for x in range(0,25)]
        for hour in time:
            self.hour_store.append([str(hour)])

        self.min_store = Gtk.ListStore(str)
        mtime = [x for x in range(0,60, 5)]
        for minute in mtime:
            self.min_store.append([str(minute)])

        self.hour_combo = Gtk.ComboBox.new_with_model_and_entry(self.hour_store)
        self.hour_combo.connect("changed", self.on_time_combo_changed, "SHOUR")
        self.hour_combo.set_entry_text_column(0)
        self.hour_combo.set_active(int(cfg['main']['SHOUR']))

        self.min_combo = Gtk.ComboBox.new_with_model_and_entry(self.min_store)
        self.min_combo.connect("changed", self.on_time_combo_changed, "SMIN")
        self.min_combo.set_entry_text_column(0)

        self.min_combo.set_active(mtime.index(int(cfg['main']['SMIN'])))

        self.button_from_close = Gtk.Button.new_with_mnemonic("_SAVE")
        self.button_from_close.connect("clicked", self.on_close_clicked, self.before_form)

        self.box_from.append(self.label_from)
        self.box_from.append(self.hour_combo)
        self.box_from.append(self.label_from_min)
        self.box_from.append(self.min_combo)
        self.box_from.append(self.button_from_close)

    def on_close_clicked(self, button, window):
        window.destroy()


    def on_time_combo_changed(self, combo, param):
        cfg = main_func()
        if combo.get_model()[combo.get_active_iter()][0] is not None:
            data = combo.get_model()[combo.get_active_iter()][0]
            if set_status(param, data):
                if 'shour' == param.lower():
                    self.button_from.set_label(f"{timecreators(data)}:{timecreators(cfg['main']['SMIN'])}")
                if 'smin' == param.lower():
                    self.button_from.set_label(f"{timecreators(cfg['main']['SHOUR'])}:{timecreators(data)}")
                if 'ehour' == param.lower():
                    self.button_to.set_label(f"{timecreators(data)}:{timecreators(cfg['main']['EMIN'])}")
                if 'emin' == param.lower():
                    self.button_to.set_label(f"{timecreators(cfg['main']['EHOUR'])}:{timecreators(data)}")

    def bto(self, bto):
        cfg = main_func()
        self.to_form = Gtk.ApplicationWindow(transient_for=app.get_active_window())
        self.to_form.set_default_size(360, 720)
        self.to_form.set_title(_("Over time"))
        self.to_form.show()

        self.box_to = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.to_form.set_child(self.box_to)
        self.label_to = Gtk.Label(label = _('Select hours:'))
        self.label_to_min = Gtk.Label(label = _('Select minutes:'))

        self.to_hour_store = Gtk.ListStore(str)
        time = [x for x in range(0,25)]
        for hour in time:
            self.to_hour_store.append([str(hour)])

        self.to_min_store = Gtk.ListStore(str)
        mtime = [x for x in range(0,60, 5)]
        for minute in mtime:
            self.to_min_store.append([str(minute)])

        self.to_hour_combo = Gtk.ComboBox.new_with_model_and_entry(self.to_hour_store)
        self.to_hour_combo.connect("changed", self.on_time_combo_changed, "EHOUR")
        self.to_hour_combo.set_entry_text_column(0)
        self.to_hour_combo.set_active(int(cfg['main']['EHOUR']))

        self.to_min_combo = Gtk.ComboBox.new_with_model_and_entry(self.to_min_store)
        self.to_min_combo.connect("changed", self.on_time_combo_changed, "EMIN")
        self.to_min_combo.set_entry_text_column(0)
        self.to_min_combo.set_active(mtime.index(int(cfg['main']['EMIN'])))

        self.button_to_close = Gtk.Button.new_with_mnemonic("_SAVE")
        self.button_to_close.connect("clicked", self.on_close_clicked, self.to_form)

        self.box_to.append(self.label_to)
        self.box_to.append(self.to_hour_combo)
        self.box_to.append(self.label_to_min)
        self.box_to.append(self.to_min_combo)
        self.box_to.append(self.button_to_close)


    def show_about(self, action=None, param=None):
        self.dialog = Adw.AboutWindow(transient_for=app.get_active_window())
        self.dialog.set_default_size(360, 720)
        self.dialog.set_application_name("DND Scheduler")
        self.dialog.set_version("0.2")
        self.dialog.set_developer_name("Chibiko")
        self.dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0))
        self.dialog.set_comments("Application to rule 'do not disturb' schedule for Librem 5")
        self.dialog.set_website("https://github.com/zenogears/dndscheduler")
        self.dialog.set_issue_url("https://github.com/zenogears/dndscheduler/issues")
        self.dialog.add_credit_section("Contributors", ["Chibiko"])
        self.dialog.set_translator_credits("Chibiko")
        self.dialog.set_copyright("© 2023 Chibiko")
        self.dialog.set_developers(["Chibiko"])
        self.dialog.set_application_icon("org.gnome.dndscheduler")
        self.dialog.show()

    def switch_switched(self, switch, state, param):
        set_status(param, state)
        self.label_onoff.set_text(f"Параметры запуска: {job_status('ENABLED')['text']}")


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

app = MyApp(application_id="org.gnome.dndscheduler")
app.run(sys.argv)
sm = app.get_style_manager()
sm.set_color_scheme(Adw.ColorScheme.PREFER_DARK)

