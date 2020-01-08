# create a partition in the disk using "cfdisk /dev/sda" before running the script

import os

efi="/dev/sda1"
root="/dev/sda2"
home="/dev/sda3"
swap="/dev/sda4"
swapfile=False
cpu="intel"

def exec_cmd(cmd):
    print(cmd)
    os.system(cmd)

exec_cmd("timedatectl set-ntp true")

# format partitions 
exec_cmd("mkfs.fat -F32 "+efi)
exec_cmd("mkfs.ext4 "+root)

# mount partitions
exec_cmd("mount "+root+" /mnt")
exec_cmd("mkdir /mnt/home")
exec_cmd("mount "+home+" /mnt/home")
exec_cmd("mkdir /mnt/boot")
exec_cmd("mount "+efi+" /mnt/boot")

exec_cmd("pacstrap -i /mnt base base-devel linux linux linux-firmware python man-db man-pages archlinux-keyring git "+cpu+"-ucode")

# swap
if swapfile:
    exec_cmd("genfstab -U /mnt >> /mnt/etc/fstab")
    exec_cmd("fallocate -l 4GB /mnt/swapfile")
    exec_cmd("chmod 600 /mnt/swapfile")
    exec_cmd("mkswap /mnt/swapfile")
    exec_cmd("swapon /mnt/swapfile")
    with open('/mnt/etc/fstab','a') as f:
        f.write('\n/swapfile none swap defaults 0 0')
else:
    exec_cmd("mkswap "+swap)
    exec_cmd("swapon "+swap)
    exec_cmd("genfstab -U /mnt >> /mnt/etc/fstab")

exec_cmd("mv chroot.py /mnt")
exec_cmd("arch-chroot /mnt python ./chroot.py")
exec_cmd("umount -R /mnt")