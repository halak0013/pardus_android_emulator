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
#export PATH=$HOME/.android-emulator/sdk/tools:$PATH
#export PATH=$HOME/.android-emulator/jdk-18/bin:$PATH


cd $HOME/.android-emulator/sdk

emulator -list-avds
echo "*****"
#emulator -avd armut -delete
/home/bismih/.android-emulator/sdk/platform-tools/adb devices

#/home/bismih/.android-emulator/sdk/platform-tools/adb -s emulator-5554 emu kill

#/home/bismih/.android-emulator/sdk/platform-tools/adb kill-server
#/home/bismih/.android-emulator/sdk/platform-tools/adb devices | grep emulator | cut -f1 | while read line; do /home/bismih/.android-emulator/sdk/platform-tools/adb -s $line emu kill; done
#/home/bismih/.android-emulator/sdk/platform-tools/adb -s emulator-5554 emu kill
