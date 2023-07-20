from static.comands import Commands as co
from gi.repository import GLib
import threading
import subprocess

import gi
gi.require_version("Gtk", "3.0")


class CommandRunner:
    is_thread_runnig=True
    def __init__(self, command, lb_subpro_output=None, lb_dialog_wait_status=None, fun_with_output=None, fun_with_paramaters=None):
        self.command = command
        self.lb_subpro_output = lb_subpro_output
        self.lb_dialog_wait_status = lb_dialog_wait_status
        self.fun_with_output = fun_with_output
        self.fun_with_paramaters = fun_with_paramaters
        self.output = ""

    def run_command(self):
        process = subprocess.Popen(
            self.command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            env=co.env,
        )

        while self.is_thread_runnig:
            print("comand runner")
            print(self.command)
            line = process.stdout.readline()
            if len(line) != 0:
                self.output += line #! burdadn hata verebilir bir ihtimal
            print("line: ", line, len(line))
            if not line:
                self.output = self.output.replace('\n\n', '\n')
                if self.fun_with_output != None:
                    print("cr:"+self.output)
                    for f in self.fun_with_output:
                        f(self.output)

                if self.fun_with_paramaters != None:
                    for f in self.fun_with_paramaters:
                        f()
                break

            GLib.idle_add(self.update_label, line.strip())

    def update_label(self, text):
        if self.lb_dialog_wait_status != None:
            self.lb_subpro_output.set_text(self.output)
            self.lb_dialog_wait_status.set_text(text)

    def run(self):
        threading.Thread(target=self.run_command).start()
