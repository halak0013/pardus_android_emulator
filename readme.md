# Pardus Android Emulator

Yo can:
- Generate an Android Emulator,
- Edit it,
- Delete it,
- Chose its sdk
- with google or google and playstore or without google and playstore

<img src="data/pardus-android-emulator.svg" width="200" style="display: block; margin-left: auto; margin-right: auto;">

![main](data/img/main.png)

![main](data/img/edit.png)

![main](data/img/new_device.png)

## Dependencies

`pip install -r requirements.txt`

# Runnig

`python3 main.py`

# Building

```console
sudo apt install devscripts git-buildpackage
sudo mk-build-deps -ir
gbp buildpackage --git-export-dir=/tmp/build/pardus-android-emulator -us -uc --git-ignore-branch --git-ignore-new

```