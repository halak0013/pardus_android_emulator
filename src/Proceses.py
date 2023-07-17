from gi.repository import GLib, Gtk
from src.CommandRunner import CommandRunner
from src.static.comands import Commands as co

import shutil,os
import gi
gi.require_version("Gtk", "3.0")


class Proceses:
    def __init__(self, lb_subpro_output: Gtk.Label, lb_wait_status: Gtk.Label,
                 chalge_stack_page: Gtk.Stack):
        self.lb_subpro_output = lb_subpro_output
        self.lb_wait_status = lb_wait_status
        self.chalge_stack_page = chalge_stack_page
        self.avd_lst = []


    def get_init_variables(self, fn):
        self.avd_lst = []
        comand_runner = CommandRunner(
            co.avd_lst_c, self.lb_subpro_output, self.lb_wait_status, fun_with_output=[self.fill_avd_lst]+fn)
        comand_runner.run()
        del comand_runner


    def fill_avd_lst(self, output):
        self.avd_lst = output.strip().split("\n")


    def get_configuration(self):
        datas = {}
        with open(f"{co.HOME}/.android-emulator/avd/{co.avd_name}.avd/config.ini", "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("hw.keyboard ="):
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
        return datas

    def get_true_false(self,val):
        if val == "yes":
            return True
        else:
            return False
        
    def run_avd(self):
        comand_runner = CommandRunner(
            co.get_android_comand(False), self.lb_subpro_output, self.lb_wait_status, fun_with_paramaters=[
                lambda: self.go_to_page("box_main")])
        comand_runner.run()
        del comand_runner

    def delete_avd(self):
        name=co.avd_name
        if os.path.exists(f"{co.HOME}/.android-emulator/avd/{name}.avd"):
            shutil.rmtree(f"{co.HOME}/.android-emulator/avd/{name}.avd")
            os.remove(f"{co.HOME}/.android-emulator/avd/{name}.ini")

        if os.path.exists(f"{co.HOME}/.android-emulator/userdata/{name}.img"):
            os.remove(f"{co.HOME}/.android-emulator/userdata/{name}.img")
            os.remove(f"{co.HOME}/.android-emulator/userdata/{name}.img.qcow2")

    def go_to_page(self, page):
        GLib.idle_add(self.change_stack_page, page)

    def change_stack_page(self,page):
        self.chalge_stack_page.set_visible_child_name(page)

    def stop_emulator(self):
        print(co.adb_kill)
        comand_runner = CommandRunner(
            co.adb_kill, self.lb_subpro_output, self.lb_wait_status)
        comand_runner.run()
        del comand_runner