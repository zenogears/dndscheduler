import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio

from .helper import main


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        cfg = main()
        super().__init__(*args, **kwargs)
        self.set_default_size(360, 720)
        self.set_title("DND Scheduler")

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.box.set_margin_top(20)
        self.box.set_margin_start(10)
        self.box.set_margin_end(10)
        self.set_child(self.box)

        self.label_from = Gtk.Label(label="Не беспокоить с:")
        self.button_from = Gtk.Button(label=f"{cfg['main']['HOUR']}:00")

        self.label_to = Gtk.Label(label="Не беспокоить до:")
        self.button_to = Gtk.Button(label="10:00 следующего дня")

        self.label_repeat = Gtk.Label(label="Повтор:")
        self.button_repeat = Gtk.Button(label="Пн, Вт, Ср, Чт, Пт")

        self.button_about = Gtk.Button(label="О приложении")

        self.box.append(self.label_from)
        self.box.append(self.button_from)

        self.box.append(self.label_to)
        self.box.append(self.button_to)

        self.box.append(self.label_repeat)
        self.box.append(self.button_repeat)

        self.box.append(self.button_about)

        self.button_from.connect('clicked', self.bfrom)
        self.button_to.connect('clicked', self.bto)
        self.button_repeat.connect('clicked', self.brepeat)
        self.button_about.connect('clicked', self.show_about)

    def brepeat(self, brepeat):
        before_form = Gtk.ApplicationWindow(transient_for=app.get_active_window())
        before_form.set_default_size(360, 720)
        before_form.set_title("Время начала")
        before_form.show()

    def bfrom(self, bfrom):
        before_form = Gtk.ApplicationWindow(transient_for=app.get_active_window())
        before_form.set_default_size(360, 720)
        before_form.set_title("Время начала")
        before_form.show()

    def bto(self, bto):
        before_form = Gtk.ApplicationWindow(transient_for=app.get_active_window())
        before_form.set_default_size(360, 720)
        before_form.set_title("Время окончания")
        before_form.show()

    def show_about(self, action=None, param=None):
        dialog = Adw.AboutWindow(transient_for=app.get_active_window())
        dialog.set_default_size(360, 720)
        dialog.set_application_name("DND Scheduler")
        dialog.set_version("0.1")
        dialog.set_developer_name("Chibiko")
        dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0))
        dialog.set_comments("Application to rule schedule for Librem 5")
        dialog.set_website("https://github.com/zenogears/dndscheduler")
        dialog.set_issue_url("https://github.com/zenogears/dndscheduler/issues")
        dialog.add_credit_section("Contributors", ["Chibiko"])
        dialog.set_translator_credits("Chibiko")
        dialog.set_copyright("© 2023 Chibiko")
        dialog.set_developers(["Chibiko"])
        dialog.set_application_icon("org.gnome.dndscheduler")
        dialog.show()

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

app = MyApp(application_id="org.gnome.dndscheduler")
app.run(sys.argv)

