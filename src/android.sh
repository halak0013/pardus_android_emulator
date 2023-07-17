#!/bin/bash
set -e
self=$(realpath $0)  #?/home/bismih/bash
# Creating sdk directory
mkdir -p $HOME/.android-emulator/sdk  #? sdk yolunu olşuturyor
cd $HOME/.android-emulator/
# İnstalling java #? java 1.8 inidiriyor ve çıkarttıyor
if [[ ! -d $HOME/.android-emulator/jdk-18 ]] ; then
    wget -c https://download.java.net/openjdk/jdk18/ri/openjdk-18+36_linux-x64_bin.tar.gz -O java.tar.gz
    tar -xf java.tar.gz
    rm -f java.tar.gz
fi
# Environment variables
export JAVA_HOME=$HOME/.android-emulator/jdk-18
export ANDROID_SDK_ROOT=$HOME/.android-emulator/sdk
export ANDROID_EMULATOR_HOME=$HOME/.android-emulator/emulator
export ANDROID_AVD_HOME=$HOME/.android-emulator/avd
export ANDROID_USER_HOME=$HOME/.android-emulator/
export ANDROID_HOME=$HOME/.android-emulator/sdk
export PATH=$HOME/.android-emulator/sdk/cmdline-tools/latest/bin:$PATH
export PATH=$HOME/.android-emulator/sdk/platform-tools:$PATH
export PATH=$HOME/.android-emulator/sdk/emulator:$PATH
export PATH=$HOME/.android-emulator/jdk-18/bin:$PATH
# Installing sdkmanager
cd $HOME/.android-emulator/sdk
if [[ ! -f $HOME/.android-emulator/sdk/cmdline-tools/latest/bin/sdkmanager ]] ; then
    file=$(wget -O - https://developer.android.com/studio/index.html | grep commandline | \
        grep href | sed "s/.*href=\"//g;s/\".*//g" | grep linux)
    wget $file -O /tmp/cmdline-tools.zip #? tmpye bu isimle indiriyor
    unzip "/tmp/cmdline-tools.zip" #? sdk içine çıkartıyor
    rm -f /tmp/cmdline-tools.zip
    mv cmdline-tools qq #? qq diye bir dosya oluşturup cmdline-tools içine atıyor
    mkdir -p cmdline-tools #? yeniden cmdline-tools oluşturyor
    mv qq cmdline-tools/latest #? cmdline-tools/latest içine qq içindekileri atıyor
fi
# Reset language
export LANG=C
export LC_ALL=C
# Installing sdk tools
if [[ ! -d $HOME/.android-emulator/sdk/tools ]] ; then
    yes | sdkmanager --channel=0 --sdk_root=$HOME/.android-emulator/sdk tools #? sdk araçlarını yüklüyor
fi
# Fetch system image name
if [[ "$1" == "gapps" ]] ; then
    toolname=$(sdkmanager --sdk_root=$HOME/.android-emulator/sdk --list | grep "$(uname -m)" | grep "android-[0-9]*;" | \
        grep "play" | grep "google" | tail -n 1  | tr -s " " | cut -f 2 -d " " | sort -V) #? play + google
elif [[ "$1" == "aosp" ]] ; then
    toolname=$(sdkmanager --sdk_root=$HOME/.android-emulator/sdk --list | grep "$(uname -m)" | grep "android-[0-9]*;" | \
        grep -v "play" | grep -v "google" | tail -n 1  | tr -s " " | cut -f 2 -d " " | sort -V) #? xplay + xgoogle
else
    toolname=$(sdkmanager --sdk_root=$HOME/.android-emulator/sdk --list | grep "$(uname -m)" | grep "android-[0-9]*;" | \
        grep -v "play" | grep "google" | tail -n 1  | tr -s " " | cut -f 2 -d " " | sort -V) #? xplay + google
fi
# Installing system image
droidname=$(echo $toolname | cut -f 2 -d ";") #? system-images;android-32;google_apis_playstore;x86_64   -->  android-32
if [[ ! -d $HOME/.android-emulator/sdk/system-images/$droidname ]] ; then
    yes | sdkmanager --channel=0 --sdk_root=$HOME/.android-emulator/sdk "$toolname"
    yes | sdkmanager --channel=0 --sdk_root=$HOME/.android-emulator/sdk "platforms;$droidname"
fi
set_state(){
    sed -i "/$1.*/d" $HOME/.android-emulator/avd/elma.avd/config.ini
    echo "$1=$2" >> $HOME/.android-emulator/avd/elma.avd/config.ini
}
# Create & Edit config file
if [[ ! -d $HOME/.android-emulator/avd/$droidname.avd ]] ; then
    yes "" | avdmanager -v create avd --name "elma" --package "$toolname"
    set_state hw.keyboard yes #!
    set_state hw.mainKeys no
    set_state hw.ramSize 2048M #!
    set_state hw.gpu.enabled yes #!
    set_state hw.sdCard no #!
    set_state showDeviceFrame no
    set_state hw.gsmModem no #!
    set_state disk.dataPartition.size 32G #!
    set_state hw.camera.back webcam0 
    set_state hw.camera.front none
    set_state hw.cpu.ncore $(nproc) #!
    set_state skin.dynamic yes
    set_state hw.initialOrientation landscape
    set_state hw.lcd.height 720 #!
    set_state hw.lcd.width 1280 #!
    set_state hw.lcd.density 160 #!
    set_state fastboot.forceColdBoot yes
    set_state fastboot.forceFastBoot no
    set_state disk.cachePartition no
fi
# Install start script & application launcher
if [[ ! -f $HOME/.android-emulator/start-emu.sh ]] ; then
    cat $self > $HOME/.android-emulator/start-emu.sh
    chmod +x $HOME/.android-emulator/start-emu.sh
    mkdir -p $HOME/.local/share/applications/
    wget -c https://upload.wikimedia.org/wikipedia/commons/d/d7/Android_robot.svg -O $HOME/.android-emulator/icon.svg
    echo "[Desktop Entry]" > $HOME/.local/share/applications/android-emu.desktop
    echo "Version=1.0" >> $HOME/.local/share/applications/android-emu.desktop
    echo "Type=Application" >> $HOME/.local/share/applications/android-emu.desktop
    echo "Name=Android Emulator" >> $HOME/.local/share/applications/android-emu.desktop
    echo "Icon=$HOME/.android-emulator/icon.svg" >> $HOME/.local/share/applications/android-emu.desktop
    echo "Exec=\"$HOME/.android-emulator/start-emu.sh\" \"$1\"" >> $HOME/.local/share/applications/android-emu.desktop
    echo "Comment=Android Virtual Device" >> $HOME/.local/share/applications/android-emu.desktop
    echo "Categories=System;" >> $HOME/.local/share/applications/android-emu.desktop
    echo "Terminal=false" >> $HOME/.local/share/applications/android-emu.desktop
    echo "StartupWMClass=android" >> $HOME/.local/share/applications/android-emu.desktop
fi
# Creating userdata
mkdir -p $HOME/.android-emulator/userdata/
# run emulator
exec emulator -netfast -writable-system -data $HOME/.android-emulator/userdata/userdata.img  -avd "elma" -qemu -cpu host 


