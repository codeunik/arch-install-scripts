import os
import re

efi="/dev/sda1"
root="/dev/sda2"
home="/dev/sda3"
swap="/dev/sda4"
cpu="intel"
bootloader=1 # 1 for systemd-boot, 2 for GRUB
hostname='jarvis'
username='partha'

def exec_cmd(cmd):
    print(cmd)
    os.system(cmd)

# time zone setup
exec_cmd("ln -sf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime")
exec_cmd("hwclock --systohc")

# localization
with open('/etc/locale.gen','a') as f:
    f.write('en_US.UTF-8 UTF-8\nen_US ISO-8859-1\n')    
exec_cmd("locale-gen")
with open('/etc/locale.conf','a') as f:
    f.write('LANG=en_US.UTF-8\n')
    
# Network configuration
with open('/etc/hostname','a') as f:
    f.write(hostname+'\n')
with open('/etc/hosts','a') as f:
    f.write(
"""
127.0.0.1	localhost
::1		localhost
127.0.1.1	"""+hostname+""".localdomain	"""+hostname+'\n')

# Initramfs
exec_cmd("mkinitcpio -P")

# Root password
exec_cmd("passwd")
exec_cmd("useradd -m -g users -G wheel,video,audio,optical,storage,power -s /bin/bash "+username)
exec_cmd("passwd "+username)
exec_cmd("EDITOR=nano visudo")

#exec_cmd("cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.backup")
#exec_cmd("sed -i 's/^#Server/Server/' /etc/pacman.d/mirrorlist.backup")
#exec_cmd("rankmirrors -n 10 /etc/pacman.d/mirrorlist.backup > /etc/pacman.d/mirrorlist")

exec_cmd("pacman -S"
    # bootloader
    #+" grub efibootmgr"
    # network manager
    +" networkmanager network-manager-applet"
    # console programs
    +" bash-completion ranger p7zip"
    # file sharing
    +" grsync wget aria2 youtube-dl uget" # filezilla deluge
    # xorg and video drivers
    +" xorg-xinit xorg-server xf86-video-intel xf86-video-ati"
    # de or wm
    #+" i3 lightdm lightdm-gtk-greeter xclip"
    +" gnome"
    # sound server
    +" pulseaudio pulseaudio-alsa alsa-utils alsa-plugins"
    # file systems
    +" dosfstools mtools mtpfs ntfs-3g autofs"
    # text editors
    +" nano neovim" #emacs code atom
    # web browsers
    +" w3m firefox" #vivaldi chromium
    # audio/video players
    +" mplayer vlc" #spotify
    # fonts
    +" ttf-inconsolata ttf-fira-mono ttf-fira-code ttf-dejavu ttf-roboto noto-fonts ttf-ubuntu-font-family gnu-free-fonts adobe-source-code-pro-fonts ttf-linux-libertine"
    # graphics tools
    #+" blender krita inkscape gimp obs"
    # misc
    +" okular keepassxc gparted"
    # doc tools
    #+" pandoc texlive-most"
    )

# fstrim.timer 
exec_cmd("systemctl enable NetworkManager autofs.services")

#lightdm.service
exec_cmd("systemctl enable gdm")

if bootloader == 2:
    exec_cmd("grub-install --target=x86_64-efi --bootloader-id=GRUB --efi-directory=/boot")
    exec_cmd("grub-mkconfig -o /boot/grub/grub.cfg")
else:
    exec_cmd("bootctl --path=/boot install")
    with open("/boot/loader/loader.conf",'w') as f:
        f.write("default arch\ntimeout 4\nconsole-mode max\neditor no\n")
    root_blkid=os.popen("blkid "+root).read()
    root_uuid=re.search(r".*\ UUID=\"(.*)\"\ TYPE.*",root_blkid).group(1)
    with open("/boot/loader/entries/arch.conf",'w') as f:
        f.write(
            "title   Arch Linux"
            +"linux   /vmlinuz-linux"
            +"initrd  /"+cpu+"-ucode.img"
            +"initrd  /initramfs-linux.img"
            +"options root=UUID="+root_uuid+" rw\n")

exec_cmd("exit")
