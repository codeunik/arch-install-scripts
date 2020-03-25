# create a partition in the disk using "cfdisk /dev/sda" before running the script

from config import *

exec_cmd("pacman -Syy reflector")
exec_cmd(
    "reflector --latest 20 --country Sweden --country Japan --country India --country \"United States\" --country France --country Germany --age 48 --protocol https --sort rate --save /etc/pacman.d/mirrorlist"
)

exec_cmd("timedatectl set-ntp true")

# format partitions
exec_cmd("mkfs.fat -F32 " + efi)
exec_cmd("mkfs.ext4 " + root)
if format_home:
    exec_cmd("mkfs.ext4 " + home)
if not swapfile:
    exec_cmd("mkswap " + swap)
    exec_cmd("swapon " + swap)

# mount partitions
exec_cmd("mount " + root + " /mnt")
exec_cmd("mkdir /mnt/home")
exec_cmd("mount " + home + " /mnt/home")
exec_cmd("mkdir -p /mnt/boot/efi")
exec_cmd("mount " + efi + " /mnt/boot/efi")

if reinstalling:
    exec_cmd(
        "mkdir -p /mnt/var/cache/pacman/pkg/ && cp -r /mnt/home/partha/pkg/* /mnt/var/cache/pacman/pkg/"
    )

exec_cmd(
    "pacstrap -i /mnt base base-devel linux linux-firmware linux-headers python man-db man-pages git sudo pacman-contrib nano reflector "
    + cpu + "-ucode")

exec_cmd("genfstab -U /mnt >> /mnt/etc/fstab")
# swap
if swapfile:
    exec_cmd("fallocate -l {}GB /mnt/swapfile".format(swapsize))
    exec_cmd("chmod 600 /mnt/swapfile")
    exec_cmd("mkswap /mnt/swapfile")
    exec_cmd("swapon /mnt/swapfile")
    with open('/mnt/etc/fstab', 'a') as f:
        f.write('\n/swapfile none swap defaults 0 0')

exec_cmd("mv chroot.py /mnt")
exec_cmd("mv config.py /mnt")
exec_cmd("mv aur.py /mnt")
exec_cmd("arch-chroot /mnt python ./chroot.py")
exec_cmd("umount -R /mnt")
exec_cmd("reboot")
