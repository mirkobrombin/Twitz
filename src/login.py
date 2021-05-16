# login.py
#
# Copyright 2020 brombinmirko <send@mirko.pm>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, GLib, Handy, WebKit2, Soup
from .globals import cookies_path, twitch_login_uri

@Gtk.Template(resource_path='/pm/mirko/Twitz/login.ui')
class TwitzLogin(Handy.Window):
    __gtype_name__ = 'TwitzLogin'

    context = WebKit2.WebContext.get_default()
    webview = WebKit2.WebView.new_with_context(context)
    cookies = context.get_cookie_manager()
    cookiejar = Soup.CookieJarText.new(cookies_path, False)
    cookies.set_accept_policy(WebKit2.CookieAcceptPolicy.ALWAYS)
    cookiejar.set_accept_policy(Soup.CookieJarAcceptPolicy.ALWAYS)

    '''Get widgets from template'''
    scroll_window = Gtk.Template.Child()
    btn_cancel = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.set_transient_for(window)

        self.window = window
        self.settings = window.settings
        self.default_settings = window.default_settings

        self.webview.load_uri(twitch_login_uri)

        '''Signals'''
        self.btn_cancel.connect('pressed', self.close)
        self.webview.connect("load-changed", self.on_change)

        '''Cookies'''
        self.cookies.set_persistent_storage(
            cookies_path,
            WebKit2.CookiePersistentStorage.TEXT
        )

        self.scroll_window.add(self.webview)
        self.show_all()

    def close(self, widget=None):
        self.destroy()

    def on_change(self, web_view, load_event):
        cookies = self.cookiejar.all_cookies()
        for c in cookies:
            if "twitch.tv" in c.get_domain().lower():
                if c.name in ["login", "name"]:
                    self.settings.set_string("username", c.value)
                    self.window.check_login()
                    self.close()

