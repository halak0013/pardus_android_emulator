from gi.repository import GLib
import aiohttp
import zipfile
import tarfile
import os
import shutil
from time import sleep
import gi
gi.require_version('Gtk', '3.0')


class AsyncFileDownloader:
    is_thread_runnig=True
    
    def __init__(self, url):
        self.url = url
        self.file_size = 0
        self.downloaded_size = 0


    # ? async bu fonksiyon asenkron
    async def download_file(self, path, archive_file_path, extract_dir, lb_subpro_output, lb_dialog_wait_status,f_update=None):
        #self.timer = GLib.timeout_add(3000, self.up_lb)
        #GLib.idle_add(self.update_label)

        self.archive_file_path = archive_file_path
        self.extract_dir = extract_dir
        self.lb_subpro_output = lb_subpro_output
        self.lb_dialog_wait_status = lb_dialog_wait_status
        self.out_text = ""
        self.status_text = ""
        self.f_update = f_update
        self.is_downloaded = True

        async with aiohttp.ClientSession() as session:  # ? asenkron http isteklerini yönetiyor
            # ? urly bir get isteği atayoruz
            w1=True
            w2=True
            w3=True
            async with session.get(self.url) as response:
                self.file_size = int(response.headers.get('Content-Length', 0))
                path = self.url.split('/')[-1] if path == None else path

                with open(path, 'wb') as file:
                    while self.is_thread_runnig:
                        # ? içeriği 1 kb olarak okuyoz
                        chunk = await response.content.read(1024)
                        if not chunk:
                            if w1:
                                w1=False
                                sleep(5)
                                continue
                            elif w2:
                                w2=False
                                sleep(5)
                                continue
                            elif w3:
                                w3=False
                                sleep(5)
                                continue
                            else:
                                print("Network connection error")
                                break
                        
                        if self.downloaded_size == self.file_size:
                            break
                        

                        file.write(chunk)
                        self.downloaded_size += len(chunk)
                        self.status_text = f"Downloaded size: {(self.downloaded_size/1048576)}Mb"
                        if self.file_size != 0:
                            self.status_text += f"  %{self.downloaded_size/self.file_size*100}"
                        self.out_text += "\n"+self.status_text
                        print(self.status_text)
                        #GLib.idle_add(self.update_label)
        print(self.downloaded_size, self.file_size)
        if self.downloaded_size == self.file_size:
            print("Download complete!")
            self.extract_file()
            self.move_files()
            self.install_sdkm()
            print("dow 1")
            self.out_text = ""
            self.status_text = ""
            #GLib.source_remove(self.timer)
        else:
            print("Download failed!")

    def up_lb(self):
        GLib.idle_add(self.update_label)

    def update_label(self):
        self.lb_subpro_output.set_text(self.out_text)
        self.lb_dialog_wait_status.set_text(self.status_text)
        return self.is_thread_runnig
    
    def extract_file(self):
        self.out_text = ""
        status_text = ""
        try:
            if self.archive_file_path.split('.')[-1] == "zip":
                with zipfile.ZipFile(self.archive_file_path, "r") as zip_ref:
                    file_count = len(zip_ref.infolist())
                    extracted_count = 0
                    for info in zip_ref.infolist():
                        zip_ref.extract(info, self.extract_dir)
                        extracted_count += 1

                        status_text = f"Extracted size: {extracted_count}Mb"
                        if self.file_size != 0:
                            status_text += f"  %{extracted_count / file_count * 100}"
                        self.out_text += "\n"+status_text
                        #GLib.idle_add(self.update_label)

                os.remove(self.archive_file_path)
                print("arşiv dosyası başarıyla ayrıştırıldı.")

            elif self.archive_file_path.split('.')[-1] == "gz":
                with tarfile.open(self.archive_file_path, "r:gz") as tar_ref:
                    file_count = len(tar_ref.getmembers())
                    extracted_count = 0
                    for info in tar_ref.getmembers():
                        tar_ref.extract(info, self.extract_dir)
                        extracted_count += 1
                        
                        status_text = f"Extracted size: {extracted_count}Mb"
                        if self.file_size != 0:
                            status_text += f"  %{extracted_count / file_count * 100}"
                        self.out_text += "\n"+status_text
                        #GLib.idle_add(self.update_label)

                os.remove(self.archive_file_path)
                print("arşiv dosyası başarıyla ayrıştırıldı.")
        except Exception as e:
            print("arşiv dosyası ayrıştırılırken bir hata oluştu:", str(e))

    def move_files(self):
        # Dosyaları taşıma
        source_dir = os.path.join(self.extract_dir, "cmdline-tools")
        temp_dir = os.path.join(self.extract_dir, "qq")
        destination_dir = os.path.join(
            self.extract_dir, "cmdline-tools", "latest")

        # 'qq' dizinini 'cmdline-tools' dizinine taşıma
        shutil.move(source_dir, temp_dir)

        # 'latest' dizinini oluşturma
        os.makedirs(destination_dir, exist_ok=True)

        # Dosyaları 'latest' dizinine taşıma
        for item in os.listdir(temp_dir):
            item_path = os.path.join(temp_dir, item)
            shutil.move(item_path, destination_dir)

        # 'qq' dizinini silme
        os.rmdir(temp_dir)

    def install_sdkm(self):
        #GLib.source_remove(self.timer)
        self.f_update()
