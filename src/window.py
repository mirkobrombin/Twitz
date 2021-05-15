# window.py
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

import os
import webbrowser
import time
from streamlink import Streamlink
from gi.repository import Gtk, Gdk, Gio, GLib, Handy, WebKit2
from mpv import MPV, MpvRenderContext, OpenGlCbGetProcAddrFn
from pathlib import Path
from pprint import pprint
from . import chat
from . import player
from . import login
from . import preferences
from .globals import twitch_streamer_uri


@Gtk.Template(resource_path='/pm/mirko/Twitz/window.ui')
class TwitzWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'TwitzWindow'

    main_stack = Gtk.Template.Child()
    headerbar = Gtk.Template.Child()
    btn_refresh = Gtk.Template.Child()
    btn_pause = Gtk.Template.Child()
    btn_play = Gtk.Template.Child()
    btn_preferences = Gtk.Template.Child()
    btn_toggle_chat = Gtk.Template.Child()
    btn_full_chat = Gtk.Template.Child()
    btn_full_immersive = Gtk.Template.Child()
    btn_full_exit = Gtk.Template.Child()
    btn_login = Gtk.Template.Child()
    combo_res = Gtk.Template.Child()
    entry_search = Gtk.Template.Child()
    scroll_window = Gtk.Template.Child()
    sep_full_exit = Gtk.Template.Child()
    box_player = Gtk.Template.Child()
    pop_fullscreen = Gtk.Template.Child()
    frame = Gtk.Frame()

    chat = chat.TwitzChat()

    default_settings = Gtk.Settings.get_default()
    settings = Gio.Settings.new("pm.mirko.Twitz")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = player.TwitzPlayer(self)

        '''Set theme'''
        self.default_settings.set_property(
            "gtk-application-prefer-dark-theme",
            self.settings.get_boolean("dark-theme")
        )

        '''Signals'''
        self.connect("window-state-event", self.on_win_state_event)
        self.entry_search.connect('activate', self.on_search)
        self.btn_refresh.connect('pressed', self.chat.on_refresh)
        self.btn_play.connect("clicked", self.player.play)
        self.btn_pause.connect("clicked", self.player.stop)
        self.btn_preferences.connect('pressed', self.show_preferences)
        self.btn_login.connect('pressed', self.show_login)
        self.btn_toggle_chat.connect('pressed', self.toggle_chat)
        self.btn_full_chat.connect('pressed', self.set_fullscreen, "chat")
        self.btn_full_immersive.connect('pressed', self.set_fullscreen, "full")
        self.btn_full_exit.connect('pressed', self.set_fullscreen, None)
        self.combo_res.connect('changed', self.player.set_resolution)

        '''Show widgets'''
        self.frame.add(self.player)
        self.box_player.pack_start(self.frame, True, True, 0)
        self.scroll_window.add(self.chat.webview)
        self.check_login()
        self.show_all()

    def on_search(self, widget):
        streamer_name = widget.get_text()
        self.chat.set_stream(streamer_name)
        self.player.set_stream(streamer_name)
        self.main_stack.set_visible_child_name("page_stream")

    def on_win_state_event(self, widget, ev):
        self.is_fullscreen = bool(
            ev.new_window_state & Gdk.WindowState.FULLSCREEN)

    def show_preferences(self, widget):
        p = preferences.TwitzPreferences(self)
        p.present()

    def show_login(self, widget):
        l = login.TwitzLogin(self)
        l.present()

    def _toggle_fullscreen(self):
        if self.is_fullscreen:
            self.__unfullscreen()
        else:
            self.__fullscreen()

    def __fullscreen(self):
        self.headerbar.set_visible(False)
        self.fullscreen()

    def __unfullscreen(self):
        self.headerbar.set_visible(True)
        self.unfullscreen()

    def set_fullscreen(self, widget=None, status=None):
        GLib.idle_add(self.pop_fullscreen.popdown)

        for w in [self.sep_full_exit, self.btn_full_exit]:
            if status is None:
                w.set_visible(False)
            else:
                w.set_visible(True)

        if status is None:
            self.__unfullscreen()
            self.toggle_chat(status=False)
        elif status == "full":
            self.__fullscreen()
            self.toggle_chat(status=True)
        elif status == "chat":
            self.__fullscreen()
            self.toggle_chat(status=False)

    def toggle_chat(self, widget=None, status=None):
        if status is None:
            status = self.scroll_window.get_visible()
        self.scroll_window.set_visible(not status)

    def check_login(self):
        u = self.settings.get_string("username")
        if u and u not in ["None", None]:
            self.btn_login.handler_block_by_func(self.show_login)
            self.btn_login.set_label(u)
            self.chat.on_refresh()
