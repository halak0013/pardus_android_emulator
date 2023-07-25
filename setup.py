#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
import subprocess


def generate_mo_files():
    podir = "po"
    mo = []
    for po in os.listdir(podir):
        if po.endswith(".po"):
            os.makedirs("{}/{}/LC_MESSAGES".format(podir,
                        po.split(".po")[0]), exist_ok=True)
            mo_file = "{}/{}/LC_MESSAGES/{}".format(
                podir, po.split(".po")[0], "pardus-android-emulator.mo")
            msgfmt_cmd = 'msgfmt {} -o {}'.format(podir + "/" + po, mo_file)
            subprocess.call(msgfmt_cmd, shell=True)
            mo.append(("/usr/share/locale/" + po.split(".po")[0] + "/LC_MESSAGES",
                       ["po/" + po.split(".po")[0] + "/LC_MESSAGES/pardus-android-emulator.mo"]))
    return mo


changelog = "debian/changelog"
if os.path.exists(changelog):
    head = open(changelog).readline()
    try:
        version = head.split("(")[1].split(")")[0]
    except:
        print("debian/changelog format is wrong for get version")
        version = "0.0.0"
    f = open("data/version", "w")
    f.write(version)
    f.close()

data_files = [
    ("/usr/bin", ["pardus-android-emulator"]),

    ("/usr/share/applications",
     ["tr.org.pardus.android.emulator.desktop"]),  # /usr/share/icons

    ("/usr/share/icons",
     ["data/pardus-android-emulator.svg"]),

    ("/usr/share/icons/hicolor/scalable/apps/",
     ["data/pardus-android-emulator.svg"]),



    ("/usr/share/pardus/pardus-android-emulator/ui",
     ["ui/MainWindow.glade"]),

    ("/usr/share/pardus/pardus-android-emulator/src",
     ["src/AsyncFileDownloader.py",
      "src/CommandRunner.py",
      "src/Installer.py",
      "src/MainWindow.py",
      "src/Main.py",
      "src/Process.py"]),

    ("/usr/share/pardus/pardus-android-emulator/src/static",
     ["src/static/commands.py",
      "src/static/android_versions.py",
      "src/static/common_vals.py",
      ]),

    ("/usr/share/pardus/pardus-android-emulator/data",
     ["data/pardus-android-emulator.svg",
      "data/version"]),

    ("/usr/share/pardus/pardus-android-emulator/data/img",
     ["data/img/edit.png",
      "data/img/main.png",
      "data/img/new_device.png",
      "data/img/phone.png",
      ]),
] + generate_mo_files()

setup(
    name="pardus-android-emulator",
    version=version,
    packages=find_packages(),
    scripts=["pardus-android-emulator"],
    install_requires=["PyGObject", "beautifulsoup4", "aiohttp"],
    data_files=data_files,
    author="Muhammet Halak",
    author_email="halakmuhammet145@gmail.com",
    description="Generate an Android Emulator easily",
    license="GPLv3",
    keywords="pardus-android-emulator, emulator, android, pardus",
    url="https://github.com/halak0013/pardus_android_emulator",
)
