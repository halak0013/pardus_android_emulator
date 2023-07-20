#!/usr/bin/env python3

import sys
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from MainWindow import MainWindow
from AsyncFileDownloader import AsyncFileDownloader
from CommandRunner import CommandRunner


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="tr.org.pardus.android_emulator", **kwargs)

    def do_activate(self):
        self.window = MainWindow(self)

    def onExit(self,e):
        AsyncFileDownloader.is_thread_runnig=False
        CommandRunner.is_thread_runnig=False
        self.window.destroy()


app = Application()
app.run(sys.argv)