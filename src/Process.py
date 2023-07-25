from gi.repository import GLib, Gtk
from CommandRunner import CommandRunner
from static.commands import Commands as co
from static.common_vals import Common_vals as cv

import shutil
import os
import gi
gi.require_version("Gtk", "3.0")


class Processes:
    def __init__(self):
        self.lb_subpro_output = cv.lb_subpro_output
        self.lb_wait_status = cv.lb_dialog_wait_status
        self.prg_status = cv.prg_bar_process
        self.stck_main = cv.stck_main
        self.avd_lst = []

    def get_init_variables(self, fn):
        self.avd_lst = []
        command_runner = CommandRunner(
            co.avd_lst_c, fun_with_output=[self.fill_avd_lst]+fn)
        command_runner.run()
        del command_runner

    def fill_avd_lst(self, output):
        self.avd_lst = output.strip().split("\n")

    def get_configuration(self):
        datas = {}
        with open(f"{co.HOME}/.android-emulator/avd/{co.avd_name}.avd/config.ini", "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith(("hw.keyboard =", "hw.keyboard=")):
                    datas['keyboard'] = self.get_true_false(line.split()[-1])
                elif line.startswith("hw.ramSize"):
                    datas['ram'] = line.split()[-1]
                elif line.startswith("hw.gpu.enabled"):
                    datas['gpu'] = self.get_true_false(line.split()[-1])
                elif line.startswith("hw.sdCard"):
                    datas['sd_card'] = self.get_true_false(line.split()[-1])
                elif line.startswith("hw.gsmModem"):
                    datas['gsm_modem'] = self.get_true_false(line.split()[-1])
                elif line.startswith("disk.dataPartition.size"):
                    datas['disk'] = line.split()[-1]
                elif line.startswith("hw.cpu.ncore"):
                    datas['cpu_core'] = line.split()[-1]
                elif line.startswith("hw.initialOrientation"):
                    datas['orientation'] = line.split()[-1]
                elif line.startswith("hw.lcd.height"):
                    datas['display_height'] = line.split()[-1]
                elif line.startswith("hw.lcd.width"):
                    datas['display_width'] = line.split()[-1]
                elif line.startswith("hw.lcd.density"):
                    datas['density'] = line.split()[-1]
                elif line.startswith("image.sysdir.1"):
                    datas['sys_name'] = line.split("=")[-1]
        return datas

    def get_true_false(self, val):
        if val == "yes":
            return True
        else:
            return False

    def run_avd(self):
        print(co.droidname, co.toolname, co.avd_name)
        command_runner = CommandRunner(
            co.get_android_command(False), fun_with_parameters=[
                lambda: self.go_to_page("box_main")])
        command_runner.run()
        del command_runner

    def delete_avd(self):
        name = co.avd_name
        if os.path.exists(f"{co.HOME}/.android-emulator/avd/{name}.avd"):
            shutil.rmtree(f"{co.HOME}/.android-emulator/avd/{name}.avd")
        if os.path.exists(f"{co.HOME}/.android-emulator/avd/{name}.ini"):
            os.remove(f"{co.HOME}/.android-emulator/avd/{name}.ini")

        if os.path.exists(f"{co.HOME}/.android-emulator/userdata/{name}"):
            shutil.rmtree(f"{co.HOME}/.android-emulator/userdata/{name}")

    def go_to_page(self, page):
        GLib.idle_add(self.change_stack_page, page)

    def change_stack_page(self, page):
        self.stck_main.set_visible_child_name(page)

    def stop_emulator(self):
        print(co.adb_kill)
        command_runner = CommandRunner(co.adb_kill)
        command_runner.run()
        del command_runner

    def check_virtualization_support(self):
        intel_path = "/sys/module/kvm_intel/parameters/nested"
        amd_path = "/sys/module/kvm_amd/parameters/nested"

        is_support = ""
        if os.path.exists(amd_path):
            with open(amd_path, "r") as amd_file:
                is_support = amd_file.read().strip()
        elif os.path.exists(intel_path):
            with open(intel_path, "r") as intel_file:
                is_support = intel_file.read().strip()
        return True if is_support == "y" or is_support == "1" else False
