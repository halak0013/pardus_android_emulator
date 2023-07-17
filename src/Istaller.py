from gi.repository import GLib, Gtk
from src.AsyncFileDownloader import AsyncFileDownloader
from src.CommandRunner import CommandRunner
from src.static.comands import Commands as co
from bs4 import BeautifulSoup as bs
import requests
import threading,os
import asyncio
import shutil

import gi
gi.require_version("Gtk", "3.0")


class Installer:
    def __init__(self, lb_subpro_output: Gtk.Label, lb_wait_status: Gtk.Label,
                 chalge_stack_page: Gtk.Stack):
        self.gv_list = []
        self.g_list = []
        self.n_list = []


        self.lb_subpro_output = lb_subpro_output
        self.lb_wait_status = lb_wait_status
        self.chalge_stack_page = chalge_stack_page

        self.downloader = None


    def check_sdkm(self):
        if os.path.exists(co.SDK+"/cmdline-tools/latest/bin/sdkmanager"):
            return True
        else:
            if os.path.exists(co.HOME+"/.android-emulator"):
                shutil.rmtree(co.HOME+"/.android-emulator")
            return False

    def install_sdkmanager(self):
        self.cmdline_tool_init()
        url = self.get_processed_url()
        self.downloader = AsyncFileDownloader(url)
        threading.Thread(target=self.download).start()

    def download(self):
        asyncio.run(self.main())

    async def main(self):
        await self.downloader.download_file("/tmp/cmdline-tools.zip", "/tmp/cmdline-tools.zip",
                                            co.SDK, self.lb_subpro_output, self.lb_wait_status)
        # ? install sdk manager
        comand_runner = CommandRunner(
            co.cmd_install_sdk_maanger, self.lb_subpro_output, self.lb_wait_status, fun_with_output=[self.get_andorio_list])
        comand_runner.run()
        del comand_runner
        os.makedirs(co.HOME+"/.android-emulator/userdata/")

    def get_andorio_list(self, b):
        comand_runner = CommandRunner(
            co.cmd_system_image, self.lb_subpro_output, self.lb_wait_status, fun_with_output=[self.fill_android_sdk])
        comand_runner.run()
        del comand_runner

    def fill_android_sdk(self, output):
        lst = output.strip().split("\n")
        for e in lst:
            e = e.split()[0]
            if "google" in e:
                if "playstore" in e:
                    self.gv_list.append(e)
                else:
                    self.g_list.append(e)
            else:
                self.n_list.append(e)
        print(self.n_list)
        GLib.idle_add(self.change_stack_page, "box_android_chose")



    def change_stack_page(self, page):
        self.chalge_stack_page.set_visible_child_name(page)

    def cmdline_tool_init(self):
        if not os.path.exists(co.SDK):
            os.makedirs(co.SDK)
        os.chdir(co.SDK)

    def get_processed_url(self):
        url = "https://developer.android.com/studio/index.html"
        site = requests.get(url).text
        data = bs(site, "html.parser")

        processed_data = data.findAll("a",
                                      class_="button button-primary devsite-dialog-close gc-analytics-event",
                                      id="agree-button__sdk_linux_download"
                                      )
        return processed_data[0].get("href")


    def intall_system_image(self, datas: dict,fn_up):
        co.avd_name = datas["name"]
        comand_runner = CommandRunner(
            co.get_android_comand(True), self.lb_subpro_output, self.lb_wait_status, 
            fun_with_paramaters=[
                lambda: self.set_configuration(datas),
                lambda: self.go_to_main()
            ]+fn_up)
        comand_runner.run()
        del comand_runner

    def go_to_main(self,o=None):
        GLib.idle_add(self.change_stack_page, "box_main")

    def set_configuration(self, datas: dict):
        with open(f"{co.HOME}/.android-emulator/avd/{co.avd_name}.avd/config.ini", "r") as file:
            lines = file.readlines()

            new_lines = []
            for line in lines:
                if line.startswith(("hw.keyboard =","hw.keyboard=")):
                    line = f"hw.keyboard = {self.get_yes_no(datas['keyboard'])}\n"
                elif line.startswith("hw.mainKeys"):
                    line = "hw.mainKeys = no\n"
                elif line.startswith("hw.ramSize"):
                    line = f"hw.ramSize = {datas['ram']}M\n"
                elif line.startswith("hw.gpu.enabled"):
                    line = f"hw.gpu.enabled = {self.get_yes_no(datas['gpu'])}\n"
                elif line.startswith("hw.sdCard"):
                    line = f"hw.sdCard = {self.get_yes_no(datas['sd_card'])}\n"
                elif line.startswith("showDeviceFrame"):
                    line = f"showDeviceFrame = no\n"
                elif line.startswith("hw.gsmModem"):
                    line = f"hw.gsmModem = {self.get_yes_no(datas['gsm_modem'])}\n"
                elif line.startswith("disk.dataPartition.size"):
                    line = f"disk.dataPartition.size = {datas['disk']}G\n"
                elif line.startswith("hw.camera.back"):
                    line = f"hw.camera.back = webcam0\n"
                elif line.startswith("hw.camera.front"):
                    line = f"hw.camera.front = none\n"
                elif line.startswith("hw.cpu.ncore"):
                    line = f"hw.cpu.ncore = {datas['cpu_core']}\n"
                elif line.startswith("hw.initialOrientation"):
                    line = f"hw.initialOrientation = {datas['orientation']}\n"
                elif line.startswith("hw.lcd.height"):
                    line = f"hw.lcd.height = {datas['display_height']}\n"
                elif line.startswith("hw.lcd.width"):
                    line = f"hw.lcd.width = {datas['display_width']}\n"
                elif line.startswith("hw.lcd.density"):
                    line = f"hw.lcd.density = {datas['density']}\n"
                elif line.startswith("fastboot.forceColdBoot"):
                    line = f"fastboot.forceColdBoot = yes\n"
                elif line.startswith("fastboot.forceFastBoot"):
                    line = f"fastboot.forceFastBoot = no\n"
                elif line.startswith("disk.cachePartition ="):
                    line = f"disk.cachePartition = no\n"
                new_lines.append(line)

            with open(f"{co.HOME}/.android-emulator/avd/{co.avd_name}.avd/config.ini", "w") as file:
                file.writelines(new_lines)
            with open(f"{co.HOME}/.android-emulator/avd/{co.avd_name}.avd/hardware-qemu.ini", "w") as file:
                file.writelines(new_lines)

    def get_yes_no(self, val):
        if val:
            return "yes"
        else:
            return "no"


