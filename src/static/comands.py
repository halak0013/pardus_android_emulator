import os


class Commands:

    # ? envirolnments
    HOME = os.path.expanduser("~")
    SDK=HOME+"/.android-emulator/sdk"
    ADB=SDK+"/platform-tools/adb"
    env = os.environ.copy()
    env["ANDROID_SDK_ROOT"] = SDK
    env["ANDROID_EMULATOR_HOME"] = HOME+"/.android-emulator/emulator"
    env["ANDROID_AVD_HOME"] = HOME+"/.android-emulator/avd"
    env["ANDROID_USER_HOME"] = HOME+"/.android-emulator/"
    env["ANDROID_HOME"] = SDK
    env["PATH"] = SDK+"/cmdline-tools/latest/bin:" + env["PATH"]
    env["PATH"] = SDK+"/platform-tools:" + env["PATH"]
    env["PATH"] = SDK+"/emulator:" + env["PATH"]

    #env["LANG"] = "C"
    #env["LC_ALL=C"] = "C"


    cmd_install_sdk_maanger=f'''
chmod +x {SDK}/cmdline-tools/latest/bin/*
yes | sdkmanager --channel=0 --sdk_root=$HOME/.android-emulator/sdk tools
    '''
    cmd_system_image=f'sdkmanager --sdk_root={SDK} --list | grep "$(uname -m)" | grep "android-[0-9]*;"'


    toolname="" #? system-images;android-34;google_apis;x86_64
    droidname="" #? android-34
    avd_name = ""
    cmd_install_system_image = f'''
        yes | sdkmanager --channel=0 --sdk_root={SDK} "${toolname}"
        yes | sdkmanager --channel=0 --sdk_root={SDK} "platforms;${droidname}"
    '''
    avd_edit=f'yes "" | avdmanager -v create avd --name "$droidname" --package "${toolname}"'
    avd_lst_c="emulator -list-avds"

    adb_kill=f"{ADB} devices | grep emulator | cut -f1 | while read line; do {ADB} -s $line emu kill; done"

    @classmethod
    def get_android_comand(self,ins=False):
        comand=""
        if ins:
            return f'''
                yes | sdkmanager --channel=0 --sdk_root={self.SDK} "{self.toolname}"
                yes | sdkmanager --channel=0 --sdk_root={self.SDK} "platforms;{self.droidname}"
                yes "" | avdmanager -v create avd --name "{self.avd_name}" --package "{self.toolname}"
                '''
        else:
            return f'exec emulator -netfast -writable-system -data $HOME/.android-emulator/userdata/{self.avd_name}/{self.avd_name}.img  -avd "{self.avd_name}" -feature -Vulkan -qemu -cpu host'
    
    def __init__(self):
        pass