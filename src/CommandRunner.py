from static.commands import Commands as co
from static.common_vals import Common_vals as cv
from gi.repository import GLib
import threading
import subprocess
import re
import os
import signal

import gi
gi.require_version("Gtk", "3.0")


class CommandRunner:
    is_thread_running = True
    cv.is_process_running = True

    def __init__(self, command, fun_with_output=None, fun_with_parameters=None):
        self.command = command
        self.lb_subpro_output = cv.lb_subpro_output
        self.lb_dialog_wait_status = cv.lb_dialog_wait_status
        self.prg_status = cv.prg_bar_process
        self.fun_with_output = fun_with_output
        self.fun_with_parameters = fun_with_parameters
        self.output = ""
        self.is_continue = True

    def run_command(self):
        self.process = subprocess.Popen(
            self.command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            env=co.env,
        )

        while self.is_thread_running:
            print("command runner")
            print(self.command)
            line = self.process.stdout.readline()
            if len(line) != 0:
                self.output += line
            print("line: ", line, len(line))
            if not line:
                self.output = self.output.replace('\n\n', '\n')
                if self.fun_with_output != None:
                    print("cr:"+self.output)
                    for f in self.fun_with_output:
                        f(self.output)

                if self.fun_with_parameters != None:
                    for f in self.fun_with_parameters:
                        f()
                break

            GLib.idle_add(self.update_label, line.strip())
        if not self.is_thread_running:
            self.stop()

    def update_label(self, text):
        if self.lb_dialog_wait_status != None:
            percentage_pattern = r'(\d+)%'
            percentages = re.findall(percentage_pattern, text)
            self.lb_subpro_output.set_text(self.output)
            self.lb_dialog_wait_status.set_text(text)
            if len(percentages) != 0:
                print(percentages[0], "***********percent")
                self.prg_status.set_fraction(int(percentages[0])/100)

    def run(self):
        threading.Thread(target=self.run_command).start()

    def stop(self):
        cv.is_process_running = False
        pid = self.process.pid
        pgid = os.getpgid(pid)
        # Send SIGTERM to the process group to terminate the subprocess and its children
        os.killpg(pgid, signal.SIGTERM)
