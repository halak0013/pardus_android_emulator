#!/bin/bash
set -e
# generate packge folders
pkg_name="pardus-android-emulator"
pkg_version="1.0" # Sürüm numarasını burada değiştirin
pkg_dir="${pkg_name}-${pkg_version}"

rm -rf ${pkg_dir}
sleep 3

mkdir -p "${pkg_dir}/opt/${pkg_name}"
mkdir -p "${pkg_dir}/usr/bin"
mkdir -p "${pkg_dir}/usr/share/icons"
mkdir -p "${pkg_dir}/usr/share/applications"

# copy program folders
cp -r data po src ui main.py "${pkg_dir}/opt/${pkg_name}"

# copy executable program 
cp pardus-android-emulator "${pkg_dir}/usr/bin/"

# copy program icon
cp data/logo.svg "${pkg_dir}/usr/share/icons/${pkg_name}.svg"

# copy program .desktop file
cp $pkg_name.desktop "${pkg_dir}/usr/share/applications/${pkg_name}.desktop"

# copy Debian file
cp -r DEBIAN "${pkg_dir}/"



# Controll package
find "${pkg_dir}"

# generate package
dpkg-deb --build "${pkg_dir}"

echo "Debian paketi oluşturuldu: ${pkg_name}_${pkg_version}.deb"
