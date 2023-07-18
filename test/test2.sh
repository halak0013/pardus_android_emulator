#!/bin/bash


#export JAVA_HOME=$HOME/.android-emulator/jdk-18
export ANDROID_SDK_ROOT=$HOME/.android-emulator/sdk
export ANDROID_EMULATOR_HOME=$HOME/.android-emulator/emulator
export ANDROID_AVD_HOME=$HOME/.android-emulator/avd
export ANDROID_USER_HOME=$HOME/.android-emulator/
export ANDROID_HOME=$HOME/.android-emulator/sdk
export PATH=$HOME/.android-emulator/sdk/cmdline-tools/latest/bin:$PATH
export PATH=$HOME/.android-emulator/sdk/platform-tools:$PATH
export PATH=$HOME/.android-emulator/sdk/emulator:$PATH
#export PATH=$HOME/.android-emulator/jdk-18/bin:$PATH


cd $HOME/.android-emulator/sdk

#yes | sdkmanager --channel=0 --sdk_root=$HOME/.android-emulator/sdk "system-images;android-32;google_apis_playstore;x86_64"
#yes | sdkmanager --channel=0 --sdk_root=$HOME/.android-emulator/sdk "platforms;android-32"
#yes "" | avdmanager -v create avd --name "armut" --package "system-images;android-32;google_apis_playstore;x86_64"


#mkdir -p $HOME/.android-emulator/userdata/

#exec emulator -netfast -writable-system -data $HOME/.android-emulator/userdata/test571.img  -avd "test571" -feature -Vulkan -qemu 
#emulator -netfast -writable-system -data $HOME/.android-emulator/userdata/armut/armut.img  -avd "armut" -feature -Vulkan -qemu 
emulator -memory 4096 "armut"