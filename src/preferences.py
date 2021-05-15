# preferences.py
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

from gi.repository import Gtk, GLib, Handy

@Gtk.Template(resource_path='/pm/mirko/Twitz/preferences.ui')
class TwitzPreferences(Handy.PreferencesWindow):
    __gtype_name__ = 'TwitzPreferences'

    '''Get widgets from template'''
    switch_dark = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.set_transient_for(window)

        '''Common variables'''
        self.window = window
        self.settings = window.settings
        self.default_settings = window.default_settings

        '''Set widgets status from user settings'''
        self.switch_dark.set_active(self.settings.get_boolean("dark-theme"))

        '''Signal connections'''
        self.switch_dark.connect('state-set', self.toggle_dark)

    '''Toggle dark mode and store in user settings'''
    def toggle_dark(self, widget, state):
        self.settings.set_boolean("dark-theme", state)
        self.default_settings.set_property(
            "gtk-application-prefer-dark-theme", state)

