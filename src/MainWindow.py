from Istaller import Installer
from Proceses import Proceses
from static.comands import Commands as co
import locale
from locale import gettext as _
import os
import gi
from gi.repository import GLib, Gio, Gtk
gi.require_version('Gtk', '3.0')


# Translation Constants:
APPNAME = "pardus-android-emulator"
TRANSLATIONS_PATH = "/usr/share/locale"
# SYSTEM_LANGUAGE = os.environ.get("LANG")

# Translation functions:
locale.bindtextdomain(APPNAME, TRANSLATIONS_PATH)
locale.textdomain(APPNAME)
# locale.setlocale(locale.LC_ALL, SYSTEM_LANGUAGE)


class MainWindow(Gtk.Window):
    def __init__(self, application):
        # Gtk Builder
        self.application = application
        self.builder = Gtk.Builder()

        # Translate things on glade:
        self.builder.set_translation_domain(APPNAME)

        self.builder.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/../ui/MainWindow.glade")
        self.builder.connect_signals(self)

        # Add Window
        self.window: Gtk.Window = self.builder.get_object("main_window")
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.set_application(application)
        self.window.set_default_size(400, 300)
        self.window.connect('destroy', application.onExit)

        self.defineComponents()

        self.init_variables()

        self.window.show_all()
        if not self.installer.check_sdkm():
            self.dialog_sdkm.set_visible(True)
        self.stck_switcher.hide() #! for debug mode

        # Set version
        try:
            version = open("data/version").readline()
            print(version)
            self.dialog_about.set_version(version)
        except:
            pass

    def init_variables(self):

        self.installer = Installer(
            self.lb_subpro_output, self.lb_dialog_wait_status, self.stck_main)
        self.is_main = True
        self.is_edit = False
        self.proceses = Proceses(
            self.lb_subpro_output, self.lb_dialog_wait_status, self.stck_main)

        self.dialog_sdkm.set_modal(True)
        self.btn_sdkm_yes.set_sensitive(False)

        self.fill_cmb(self.cmb_device_type, [_('With Google and Play Store'),
                                             _('With Google without Play Store'),
                                             _('Without Google and Play Store')])
        self.scr_window.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.proceses.get_init_variables(
            [self.fill_avd_list, self.fill_properties])
        self.fill_cpu_cores()
        self.active_button(True)

    def defineComponents(self):
        self.btn_about: Gtk.Button = self.builder.get_object("btn_about")
        self.dialog_about: Gtk.AboutDialog = self.builder.get_object(
            "dialog_about")

        self.dialog_sdkm: Gtk.Dialog = self.builder.get_object("dialog_sdkm")
        self.btn_sdkm_yes: Gtk.Button = self.builder.get_object("btn_sdkm_yes")
        self.btn_sdkm_no: Gtk.Button = self.builder.get_object("btn_sdkm_no")
        self.chk_btn_term_accept: Gtk.CheckButton = self.builder.get_object(
            "chk_btn_term_accept")

        self.dialog_wait: Gtk.Dialog = self.builder.get_object("dialog_wait")
        self.btn_wait_next: Gtk.Button = self.builder.get_object(
            "btn_wait_next")
        self.btn_wait_cancel: Gtk.Button = self.builder.get_object(
            "btn_wait_cancel")

        self.stck_main: Gtk.Stack = self.builder.get_object("stck_main")
        self.stck_switcher: Gtk.StackSwitcher = self.builder.get_object("stck_switcher")

        self.box_main: Gtk.Box = self.builder.get_object("box_main")
        self.box_wait: Gtk.Box = self.builder.get_object("box_wait")
        self.box_android_chose: Gtk.Box = self.builder.get_object(
            "box_android_chose")
        self.box_set_properties: Gtk.Box = self.builder.get_object(
            "box_set_properties")

        self.lb_subpro_output: Gtk.Label = self.builder.get_object(
            "lb_subpro_output")
        self.lb_dialog_wait_status: Gtk.Label = self.builder.get_object(
            "lb_dialog_wait_status")

        self.cmb_sdk_v: Gtk.ComboBoxText = self.builder.get_object("cmb_sdk_v")
        self.cmb_device_type: Gtk.ComboBoxText = self.builder.get_object(
            "cmb_device_type")
        self.btn_and_chose_next: Gtk.Button = self.builder.get_object(
            "btn_and_chose_next")
        self.btn_and_chose_back: Gtk.Button = self.builder.get_object(
            "btn_and_chose_back")
        self.btn_set_pro_next: Gtk.Button = self.builder.get_object(
            "btn_set_pro_next")
        self.btn_set_pro_back: Gtk.Button = self.builder.get_object(
            "btn_set_pro_back")

        self.spn_ram: Gtk.Spinner = self.builder.get_object("spn_ram")
        self.spn_disk: Gtk.Spinner = self.builder.get_object("spn_disk")
        self.spn_display_height: Gtk.Spinner = self.builder.get_object(
            "spn_display_height")
        self.spn_display_width: Gtk.Spinner = self.builder.get_object(
            "spn_display_width")
        self.spn_density: Gtk.Spinner = self.builder.get_object("spn_density")
        self.chk_keyboard: Gtk.CheckButton = self.builder.get_object(
            "chk_keyboard")
        self.chk_gpu: Gtk.CheckButton = self.builder.get_object("chk_gpu")
        self.chk_sd_card: Gtk.CheckButton = self.builder.get_object(
            "chk_sd_card")
        self.chk_gsm_modem: Gtk.CheckButton = self.builder.get_object(
            "chk_gsm_modem")
        self.cmb_cpu: Gtk.ComboBoxText = self.builder.get_object(
            "cmb_cpu")

        self.btn_new_virt_android: Gtk.Button = self.builder.get_object(
            "btn_new_virt_android")

        self.lb_ram_p: Gtk.Label = self.builder.get_object("lb_ram_p")
        self.lb_disk_par_p: Gtk.Label = self.builder.get_object(
            "lb_disk_par_p")
        self.lb_hegiht_p: Gtk.Label = self.builder.get_object("lb_hegiht_p")
        self.lb_width_p: Gtk.Label = self.builder.get_object("lb_width_p")
        self.lb_desity_p: Gtk.Label = self.builder.get_object("lb_desity_p")
        self.lb_keyboard_p: Gtk.Label = self.builder.get_object(
            "lb_keyboard_p")
        self.entry_name: Gtk.Entry = self.builder.get_object("entry_name")
        self.lb_gpu_p: Gtk.Label = self.builder.get_object("lb_gpu_p")
        self.lb_sd_card_p: Gtk.Label = self.builder.get_object("lb_sd_card_p")
        self.lb_gsm_p: Gtk.Label = self.builder.get_object("lb_gsm_p")
        self.lb_cpu_p: Gtk.Label = self.builder.get_object("lb_cpu_p")
        self.rd_btn_portrait: Gtk.RadioButton = self.builder.get_object(
            "rd_btn_portrait")
        self.rd_btn_landscape: Gtk.RadioButton = self.builder.get_object(
            "rd_btn_landscape")
        self.lb_sys_name: Gtk.Label = self.builder.get_object("lb_sys_name")

        self.btn_force_stop: Gtk.Button = self.builder.get_object(
            "btn_force_stop")
        self.btn_stop: Gtk.Button = self.builder.get_object("btn_stop")
        self.btn_start: Gtk.Button = self.builder.get_object("btn_start")
        self.btn_edit: Gtk.Button = self.builder.get_object("btn_edit")
        self.btn_delete: Gtk.Button = self.builder.get_object("btn_delete")
        self.scr_window: Gtk.ScrolledWindow = self.builder.get_object(
            "scr_window")
        self.lst_virt_mach: Gtk.ListBox = self.builder.get_object(
            "lst_virt_mach")

    def fill_cmb(self, cmb, lst, is_spacial=False):
        cmb.remove_all()
        for c in lst:
            if is_spacial:
                cmb.append_text(c.split(";")[1].title())
            else:
                cmb.append_text(str(c))
        cmb.set_active(0)

    def fill_avd_list(self, o=None):
        for child in self.lst_virt_mach.get_children():
            self.lst_virt_mach.remove(child)
        for r in self.proceses.avd_lst:
            print("r: ", r)
            self.lst_virt_mach.add(Gtk.Label(label=r))
        self.lst_virt_mach.show_all()
        first_row = self.lst_virt_mach.get_row_at_index(0)
        self.lst_virt_mach.select_row(first_row)
        GLib.idle_add(self.avd_emmty_btn,self.proceses.avd_lst[0])


    def get_spn_properties(self):
        res = {}
        res["ram"] = int(self.spn_ram.get_value())
        res["disk"] = int(self.spn_disk.get_value())
        res["display_height"] = int(self.spn_display_height.get_value())
        res["display_width"] = int(self.spn_display_width.get_value())
        res["density"] = int(self.spn_density.get_value())
        res["keyboard"] = self.chk_keyboard.get_active()
        res["gpu"] = self.chk_gpu.get_active()
        res["sd_card"] = self.chk_sd_card.get_active()
        res["gsm_modem"] = self.chk_gsm_modem.get_active()
        res["cpu_core"] = self.cmb_cpu.get_active_text()
        res["orientation"] = "portrait" if self.rd_btn_portrait.get_active(
        ) else "landscape"
        res["name"] = self.entry_name.get_text()
        return res
    
    def fill_properties(self, o=None):
        if len(self.proceses.avd_lst) != 0:
            co.avd_name = self.lst_virt_mach.get_selected_row().get_child().get_text()
            print(co.avd_name, "****")
            if co.avd_name != "":
                datas = self.proceses.get_configuration()
                if not self.is_main:
                    self.entry_name.set_text(co.avd_name)
                    self.spn_ram.set_value(float(datas["ram"][:-1]))
                    self.spn_disk.set_value(float(datas["disk"][:-1]))
                    self.spn_display_height.set_value(
                        float(datas["display_height"]))
                    self.spn_display_width.set_value(float(datas["display_width"]))
                    self.spn_density.set_value(float(datas["density"]))
                    self.chk_keyboard.set_active((datas["keyboard"]))
                    self.chk_gpu.set_active(datas["gpu"])
                    self.chk_sd_card.set_active(datas["sd_card"])
                    self.chk_gsm_modem.set_active(datas["gsm_modem"])
                    self.cmb_cpu.set_active(float(datas["cpu_core"])-1)
                    self.rd_btn_portrait.set_active(
                        datas["orientation"] == "portrait")
                else:
                    self.lb_ram_p.set_text(datas["ram"])
                    self.lb_disk_par_p.set_text(datas["disk"])
                    self.lb_hegiht_p.set_text(datas["display_height"])
                    self.lb_width_p.set_text(datas["display_width"])
                    self.lb_desity_p.set_text(datas["density"])
                    self.lb_keyboard_p.set_text(str(datas["keyboard"]))
                    self.lb_gpu_p.set_text(str(datas["gpu"]))
                    self.lb_sd_card_p.set_text(str(datas["sd_card"]))
                    self.lb_gsm_p.set_text(str(datas["gsm_modem"]))
                    self.lb_cpu_p.set_text(datas["cpu_core"])
                    self.lb_sys_name.set_text(datas["sys_name"])

    def active_button(self, val: bool):
        self.btn_new_virt_android.set_sensitive(val)
        self.btn_edit.set_sensitive(val)
        self.btn_delete.set_sensitive(val)
        self.btn_start.set_sensitive(val)
        self.btn_stop.set_sensitive(not val)

    def avd_emmty_btn(self, output):
        if output!="":
            val=True
        else:
            val=False
        self.btn_edit.set_sensitive(val)
        self.btn_delete.set_sensitive(val)
        self.btn_start.set_sensitive(val)
        self.btn_force_stop.set_sensitive(val)
        self.btn_stop.set_sensitive(val)

    def fill_cpu_cores(self):
        self.fill_cmb(self.cmb_cpu, range(1, os.cpu_count()+1))

    def fill_sdks(self,index=0):
        if index == 0:
            self.fill_cmb(self.cmb_sdk_v, self.installer.gv_list, True)
            co.toolname = self.installer.gv_list[index]
        elif index == 1:
            self.fill_cmb(self.cmb_sdk_v, self.installer.g_list, True)
        elif index == 2:
            self.fill_cmb(self.cmb_sdk_v, self.installer.n_list, True)

    def is_same_avd(self):
        name=self.entry_name.get_text()
        for a in self.proceses.avd_lst:
            if name == a:
                self.entry_name.set_text("")
                self.entry_name.set_placeholder_text(_("Please type different name"))
                return False
        return True
    
    def is_word(self):
        name=self.entry_name.get_text()
        Turkish_c="ğĞıİşŞüÜöÖçÇ"
        if any(char.isspace() for char in name):
            self.entry_name.set_text("")
            self.entry_name.set_placeholder_text(_("Please don't type whitespace"))
            return False
        elif any(not char.isalnum() and not char.isspace() for char in name) or bool(set(name).intersection(set(Turkish_c))):
            self.entry_name.set_text("")
            self.entry_name.set_placeholder_text(_("Please don't type spacial chracter(.*/şüİ~)"))
            return False
        return True
    
    def on_btn_about_clicked(self, b):
        self.dialog_about.set_visible(True)

    def on_btn_sdkm_no_clicked(self, b):
        self.window.destroy()

    def on_btn_sdkm_yes_clicked(self, b):
        self.stck_main.set_visible_child_name("box_wait")
        self.installer.install_sdkmanager(self.fill_sdks)
        self.dialog_sdkm.set_visible(False)

    def on_cmb_device_type_changed(self, c: Gtk.ComboBox):
        try:
            index = c.get_active()
            self.fill_sdks(index)
        except Exception as e:
            print(e)


    def on_chk_btn_term_accept_toggled(self, b):
        if b.get_active():
            self.btn_sdkm_yes.set_sensitive(True)
        else:
            self.btn_sdkm_yes.set_sensitive(False)

    def on_btn_new_virt_android_clicked(self, b):
        self.is_main = True
        self.entry_name.set_sensitive(True)
        self.lb_dialog_wait_status=_("Waiting to get andorid sdk list...")
        self.lb_subpro_output=_("Waiting to get andorid sdk list...")
        self.stck_main.set_visible_child_name("box_wait")
        self.installer.get_andorio_list([self.fill_sdks])

    def on_btn_force_stop_clicked(self, b):
        self.active_button(True)
        self.proceses.stop_emulator()

    def on_btn_stop_clicked(self, b):
        self.active_button(True)
        self.proceses.stop_emulator()

    def on_btn_start_clicked(self, b):
        self.active_button(False)
        self.proceses.run_avd()

    def on_btn_edit_clicked(self, b):
        self.is_main = False
        self.entry_name.set_sensitive(False)
        self.fill_properties()
        self.stck_main.set_visible_child_name("box_set_properties")

    def on_btn_delete_clicked(self, b):
        self.proceses.delete_avd()
        self.proceses.get_init_variables(
            [self.fill_avd_list, self.fill_properties])

    def on_lst_virt_mach_row_activated(self, list_box, row):
        selected_label = row.get_child()
        selected_text = selected_label.get_text()
        co.avd_name = selected_text
        print(f"sellected avd: {selected_text}")
        self.fill_properties()

    def on_btn_set_pro_next_clicked(self, b):
        if self.is_main:  # ? sdk ile yeni oluştur
            if self.is_same_avd() and self.is_word():
                self.stck_main.set_visible_child_name("box_wait")
                self.installer.intall_system_image(self.get_spn_properties(), fn_up=[
                    lambda: self.proceses.get_init_variables(
                        [self.fill_avd_list, self.fill_properties])
                ])
        else:  # ? düzenleme
            self.is_main = True
            self.installer.set_configuration(self.get_spn_properties())
            self.fill_properties()
            self.stck_main.set_visible_child_name("box_main")
    
    def on_btn_set_pro_back_clicked(self,b):
        if self.is_main:  # ? sdk ile yeni oluştur
            self.stck_main.set_visible_child_name("box_android_chose")
        else:  # ? düzenleme
            self.stck_main.set_visible_child_name("box_main")

    def on_btn_and_chose_next_clicked(self, b):
        index =self.cmb_device_type.get_active()
        index2=self.cmb_sdk_v.get_active()
        if index == 0:
            co.toolname = self.installer.gv_list[index2]
        elif index == 1:
            co.toolname = self.installer.g_list[index2]
        elif index == 2:
            co.toolname = self.installer.n_list[index2]
        co.droidname = co.toolname.split(";")[1]
        print(co.toolname, co.droidname)
        self.stck_main.set_visible_child_name("box_set_properties")

    def on_btn_and_chose_back_clicked(self,b):
        self.stck_main.set_visible_child_name("box_main")


    def destroy(self):
        #TODO: çıkarken emulatör açık kalsın mı sor
        if os.path.exists(co.SDK+"/cmdline-tools/latest/bin/sdkmanager"):
            self.proceses.stop_emulator()
        self.window.destroy()
