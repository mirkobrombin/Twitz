# chat.py
#
# Copyright 2021 Mirko Brombin
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

import webbrowser
from gi.repository import Gtk, Gdk, Gio, Handy, WebKit2
from .globals import cookies_path, twitch_streamer_uri, twitch_chat_uri

twitch_uri = "https://twitch.tv"


class TwitzWebSettings(WebKit2.Settings):

    hw_accell = WebKit2.HardwareAccelerationPolicy.ON_DEMAND

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_hardware_acceleration_policy(self.hw_accell)
        self.set_enable_back_forward_navigation_gestures(True)
        self.set_enable_dns_prefetching(True)
        self.set_enable_media_capabilities(True)
        # self.set_enable_smooth_scrolling(True)
        # self.set_enable_developer_extras(True)


class TwitzContentManager(WebKit2.UserContentManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        '''CSS tricks
        style = Gio.resources_lookup_data("/pm/mirko/Twitz/inject.css", 0)
        self.add_style_sheet(
            WebKit2.UserStyleSheet(
                str(style.get_data(), "utf-8"),
                WebKit2.UserContentInjectedFrames.TOP_FRAME,
                WebKit2.UserStyleLevel.USER,
                None, None
            )
        )'''


class TwitzChat():

    context = WebKit2.WebContext.get_default()
    manager = TwitzContentManager()
    settings = TwitzWebSettings()
    policies = WebKit2.WebsitePolicies(autoplay=WebKit2.AutoplayPolicy.ALLOW)
    webview = WebKit2.WebView(
        settings=settings,
        user_content_manager=manager,
        website_policies=policies
    )
    cookies = context.get_cookie_manager()
    cookies.set_accept_policy(WebKit2.CookieAcceptPolicy.ALWAYS)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        '''Webview'''
        self.webview.set_background_color(Gdk.RGBA(0.05, 0.05, 0.05, 1.0))

        '''Cookies'''
        self.cookies.set_persistent_storage(
            cookies_path,
            WebKit2.CookiePersistentStorage.TEXT
        )

    '''Webview methods'''

    def hit_element(self, widget=None, element="body"):
        script = f"document.querySelector('{element}').click();"
        self.webview.run_javascript(script)

    def open_url(self, widget=None, url=twitch_uri):
        self.webview.load_uri(url)

    def set_stream(self, streamer_name:str):
        self.webview.load_uri(twitch_chat_uri % streamer_name)

    def on_refresh(self, widget=None):
        self.webview.reload()


