# IOTrees

Raspberry Pi Setup
==================

Emulation
---------

The Raspberry Pi can be slow to work with, for example when installing
opencv. You can emulate the Pi on your Linux computer and run CPU-intensive commands
locally. Here's how ([taken from here](jkullick)):

    sudo apt-get install qemu qemu-user-static binfmt-support

    # Follow these steps to set up a Pi image
    dd if=/dev/zero bs=1M count=1024 >> raspbian-stretch.img
    sudo losetup -P /dev/loop0 raspbian-stretch.img
    sudo e2fsck -f /dev/loop0p2
    sudo fdisk /dev/loop0
    # See https://raspberrypi.stackexchange.com/a/501 for resizing with fdisk if
    # below command complains about nothing to do
    sudo resize2fs /dev/loop0p2

    # Otherwise, if you're emulating directly from an SD card, follow just these directions,
    # and use the mounted SD card path instead of `/dev/loop0` (e.g. `/media/$USER/rootfs/`.

    sudo mount -o rw /dev/loop0p2  /mnt
    sudo mount -o rw /dev/loop0p1 /mnt/boot
    sudo mount --bind /dev /mnt/dev/
    sudo mount --bind /sys /mnt/sys/
    sudo mount --bind /proc /mnt/proc/
    sudo mount --bind /dev/pts /mnt/dev/pts
    sudo sed -i 's/^/#/g' /mnt/etc/ld.so.preload
    sudo cp /usr/bin/qemu-arm-static /mnt/usr/bin/
    sudo chroot /mnt /bin/bash

You should now be in an emulated shell. When you are finished, run these teardown commands:

    sudo sed -i 's/^#//g' /mnt/etc/ld.so.preload
    sudo umount /mnt/{dev/pts,dev,sys,proc,boot,}
    sudo losetup -d /dev/loop0

[jkullick]: https://gist.github.com/jkullick/9b02c2061fbdf4a6c4e8a78f1312a689


Setup
-----

Follow the instructions here to set up the Pi with OpenCV:

https://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/


Local Development Setup
=======================

### Repository

Clone this repository with:

    git clone https://github.com/sjruprecht/IOTrees.git


### Virtual Environment

#### Setting up

1. Install [pipenv](https://docs.pipenv.org/):

       sudo pip install pipenv

1. Inside the project directory, use `pipenv` with python 3.6 to create a virtual environment:

       cd IOTrees
       pipenv install --python $(which python3.6) --ignore-pipfile --dev

1. Activate the virtual environment:

       pipenv shell

1. Set up paths inside of the virtual environment:

       pipenv run pip install -e .

#### Usage

You can now either run a command in the virtual environment by prefixing it with `pipenv run`, or by activating a
shell inside of the virtual environment.

    # Run a command without having activated the shell
    pipenv run python foo

    # Or activate the shell first, then run a command
    pipenv shell
    python foo

There are two commands available in this repository. Example usages:

    # This detects EABs in the given image, saves debug images, and prints the number found
    detect --image examples/EAB-on-purple-trap.jpg --debug-images

    # This runs the above detection, and then sends that information to the given serial port
    eab_find --image examples/EAB-on-purple-trap.jpg --tty /dev/tty

If you get an error about command not found, make sure that you have the virtual environment activated
and that you've run `pipenv run pip install -e .`.