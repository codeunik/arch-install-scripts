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

#exec_cmd("pacman -S pacman-contrib") # for rankmirrors
#exec_cmd("cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.backup")
#exec_cmd("awk '/^## India$/{f=1; next}f==0{next}/^$/{exit}{print substr($0, 1);}' /etc/pacman.d/mirrorlist.backup")
##exec_cmd("sed -i 's/^#Server/Server/' /etc/pacman.d/mirrorlist.backup")
#exec_cmd("rankmirrors -n 6 /etc/pacman.d/mirrorlist.backup > /etc/pacman.d/mirrorlist")

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
exec_cmd("mkdir -p /mnt/var/cache/pacman/pkg/ && cp -r /mnt/home/partha/pkg/* /mnt/var/cache/pacman/pkg/")
exec_cmd("pacstrap -i /mnt base base-devel linux linux linux-firmware python man-db man-pages archlinux-keyring git sudo  pacman-contrib nano "+cpu+"-ucode")

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
exec_cmd("reboot")
