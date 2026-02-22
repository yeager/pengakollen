import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib, Gdk, Gio
import gettext, locale, os, json, time, random
__version__ = "0.1.0"

APP_ID = "se.danielnylander.pengakollen"
LOCALE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'share', 'locale')
if not os.path.isdir(LOCALE_DIR): LOCALE_DIR = '/usr/share/locale'
try:
    locale.bindtextdomain(APP_ID, LOCALE_DIR)
    gettext.bindtextdomain(APP_ID, LOCALE_DIR)
    gettext.textdomain(APP_ID)
except Exception: pass
_ = gettext.gettext
def N_(s): return s

COINS = [
    {'name': N_('1 kr'), 'value': 1, 'icon': '🪙'},
    {'name': N_('2 kr'), 'value': 2, 'icon': '🪙'},
    {'name': N_('5 kr'), 'value': 5, 'icon': '🪙'},
    {'name': N_('10 kr'), 'value': 10, 'icon': '🪙'},
]
BILLS = [
    {'name': N_('20 kr'), 'value': 20, 'icon': '💵'},
    {'name': N_('50 kr'), 'value': 50, 'icon': '💵'},
    {'name': N_('100 kr'), 'value': 100, 'icon': '💵'},
]
ITEMS = [
    {'name': N_('Apple'), 'price': 5, 'icon': '🍎'},
    {'name': N_('Juice'), 'price': 15, 'icon': '🧃'},
    {'name': N_('Sandwich'), 'price': 30, 'icon': '🥪'},
    {'name': N_('Ice cream'), 'price': 25, 'icon': '🍦'},
    {'name': N_('Book'), 'price': 50, 'icon': '📚'},
    {'name': N_('Toy'), 'price': 75, 'icon': '🧸'},
]

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title(_('Pengakollen'))
        self.set_default_size(500, 550)
        self._wallet = 0
        self._target = None

        header = Adw.HeaderBar()
        menu_btn = Gtk.MenuButton(icon_name='open-menu-symbolic')
        menu = Gio.Menu()
        menu.append(_('About'), 'app.about')
        menu_btn.set_menu_model(menu)
        header.pack_end(menu_btn)

        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        main.append(header)

        # Target item
        self._target_label = Gtk.Label()
        self._target_label.add_css_class('title-2')
        self._target_label.set_margin_top(16)
        main.append(self._target_label)

        self._wallet_label = Gtk.Label()
        self._wallet_label.add_css_class('title-3')
        main.append(self._wallet_label)

        self._feedback = Gtk.Label()
        self._feedback.add_css_class('title-4')
        main.append(self._feedback)

        # Money buttons
        money_label = Gtk.Label(label=_('Add money:'), xalign=0)
        money_label.set_margin_start(16)
        money_label.add_css_class('title-4')
        main.append(money_label)

        money_box = Gtk.FlowBox()
        money_box.set_max_children_per_line(7)
        money_box.set_selection_mode(Gtk.SelectionMode.NONE)
        money_box.set_margin_start(16)
        money_box.set_margin_end(16)
        for m in COINS + BILLS:
            btn = Gtk.Button(label=f"{m['icon']} {_(m['name'])}")
            btn.add_css_class('pill')
            btn.connect('clicked', self._add_money, m['value'])
            money_box.insert(btn, -1)
        main.append(money_box)

        # Controls
        ctrl = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        ctrl.set_halign(Gtk.Align.CENTER)
        ctrl.set_margin_top(8)
        pay_btn = Gtk.Button(label=_('Pay!'))
        pay_btn.add_css_class('suggested-action')
        pay_btn.add_css_class('pill')
        pay_btn.connect('clicked', self._pay)
        ctrl.append(pay_btn)
        reset_btn = Gtk.Button(label=_('Reset'))
        reset_btn.add_css_class('pill')
        reset_btn.connect('clicked', lambda b: self._new_item())
        ctrl.append(reset_btn)
        main.append(ctrl)

        self.set_content(main)
        self._new_item()

    def _new_item(self):
        self._target = random.choice(ITEMS)
        self._wallet = 0
        self._target_label.set_text(f"{self._target['icon']}  {_(self._target['name'])} — {self._target['price']} kr")
        self._wallet_label.set_text(_('Your money: %d kr') % self._wallet)
        self._feedback.set_text('')

    def _add_money(self, btn, value):
        self._wallet += value
        self._wallet_label.set_text(_('Your money: %d kr') % self._wallet)

    def _pay(self, btn):
        price = self._target['price']
        if self._wallet == price:
            self._feedback.set_text(_('Perfect! Exact amount! 🌟'))
        elif self._wallet > price:
            change = self._wallet - price
            self._feedback.set_text(_('You get %d kr back! 💰') % change)
        else:
            need = price - self._wallet
            self._feedback.set_text(_('You need %d kr more') % need)

class App(Adw.Application):
    def __init__(self):
        super().__init__(application_id='se.danielnylander.pengakollen')
        self.connect('activate', lambda a: MainWindow(application=a).present())
        about = Gio.SimpleAction.new('about', None)
        about.connect('activate', lambda a,p: Adw.AboutDialog(application_name=_('Pengakollen'),
            application_icon=APP_ID, version=__version__, developer_name='Daniel Nylander',
            website='https://github.com/yeager/pengakollen', license_type=Gtk.License.GPL_3_0,
            comments=_('Learn about money')).present(self.get_active_window()))
        self.add_action(about)

def main(): App().run()
if __name__ == '__main__': main()

