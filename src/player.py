# player.py
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

import ctypes
import webbrowser
from gi.repository import Gtk, Gdk, Gio, GLib, Handy, WebKit2
from OpenGL import GL, GLX
from .globals import cookies_path, twitch_streamer_uri, twitch_chat_uri
from mpv import MPV, MpvRenderContext, OpenGlCbGetProcAddrFn

def get_process_address(_, name):
    address = GLX.glXGetProcAddress(name.decode("utf-8"))
    return ctypes.cast(address, ctypes.c_void_p).value

class TwitzPlayer(Gtk.GLArea):

    stream = {
        "name": "",
        "url": "",
        "resolutions": []
    }

    def __init__(self, **properties):
        super().__init__(**properties)

        self._proc_addr_wrapper = OpenGlCbGetProcAddrFn(get_process_address)
        self.ctx = None
        self.mpv = MPV()

        self.connect("realize", self.on_realize)
        self.connect("render", self.on_render)
        self.connect("unrealize", self.on_unrealize)

    def set_stream(self, streamer_name:str):
        self.stream = {
            "name": streamer_name,
            "url": twitch_streamer_uri % streamer_name,
            "resolutions": []
        }
        self.play()

    def stop(self, widget=None, data=None):
        self.mpv.stop()

    def play(self, widget=None, data=None):
        self.mpv.play(self.stream["url"])

    def on_realize(self, widget, data=None):
        self.make_current()
        self.ctx = MpvRenderContext(
            self.mpv,
            'opengl',
            opengl_init_params={
                'get_proc_address': self._proc_addr_wrapper
            }
        )
        self.ctx.update_cb = self.wrapped_c_render_func

    def on_unrealize(self, arg):
        self.ctx.free()
        self.mpv.terminate()

    def wrapped_c_render_func(self):
        GLib.idle_add(self.call_frame_ready, None, GLib.PRIORITY_HIGH)

    def call_frame_ready(self, *args):
        if self.ctx.update():
            self.queue_render()

    def on_render(self, arg1, arg2):
        if self.ctx:
            factor = self.get_scale_factor()
            rect = self.get_allocated_size()[0]

            width = rect.width * factor
            height = rect.height * factor

            fbo = GL.glGetIntegerv(GL.GL_DRAW_FRAMEBUFFER_BINDING)
            self.ctx.render(
                flip_y=True,
                opengl_fbo={
                    'w': width,
                    'h': height,
                    'fbo': fbo
                }
            )
            return True

        return False
        
