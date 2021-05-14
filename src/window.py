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
from gi.repository import Gtk, Gdk, Gio, Handy, WebKit2
from mpv import MPV, MpvRenderContext, OpenGlCbGetProcAddrFn
from pathlib import Path
from pprint import pprint
from . import chat
from . import player
from . import preferences
from .globals import twitch_streamer_uri


@Gtk.Template(resource_path='/pm/mirko/Twitz/window.ui')
class TwitzWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'TwitzWindow'

    main_stack = Gtk.Template.Child()
    btn_refresh = Gtk.Template.Child()
    btn_pause = Gtk.Template.Child()
    btn_play = Gtk.Template.Child()
    btn_preferences = Gtk.Template.Child()
    btn_toggle_chat = Gtk.Template.Child()
    combo_res = Gtk.Template.Child()
    entry_search = Gtk.Template.Child()
    scroll_window = Gtk.Template.Child()
    box_player = Gtk.Template.Child()
    frame = Gtk.Frame()

    default_settings = Gtk.Settings.get_default()
    settings = Gio.Settings.new("pm.mirko.Twitz")

    chat = chat.TwitzChat()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = player.TwitzPlayer(self)

        '''Prefer dark theme'''
        self.default_settings.set_property(
            "gtk-application-prefer-dark-theme",
            True
        )

        '''Signals'''
        self.entry_search.connect('activate', self.on_search)
        self.btn_refresh.connect('pressed', self.chat.on_refresh)
        self.btn_play.connect("clicked", self.player.play)
        self.btn_pause.connect("clicked", self.player.stop)
        self.btn_preferences.connect('pressed', self.show_preferences)
        self.btn_toggle_chat.connect('pressed', self.toggle_chat)
        self.combo_res.connect('changed', self.player.set_resolution)

        self.frame.add(self.player)
        self.box_player.pack_start(self.frame, True, True, 0)

        '''Show widgets'''
        self.scroll_window.add(self.chat.webview)
        self.show_all()

    def on_search(self, widget):
        streamer_name = widget.get_text()
        self.player.set_stream(streamer_name)
        self.chat.set_stream(streamer_name)

    def show_preferences(self, widget):
        p = preferences.TwitzPreferences(self)
        p.present()

    def toggle_chat(self, widget):
        status = self.scroll_window.get_visible()
        self.scroll_window.set_visible(not status)

