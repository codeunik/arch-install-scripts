import os
import re
from config import *

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
##exec_cmd("sed -i 's/^#Server/Server/' /etc/pacman.d/mirrorlist.backup")
#exec_cmd("awk '/^## India$/{f=1; next}f==0{next}/^$/{exit}{print substr($0, 1);}' /etc/pacman.d/mirrorlist.backup")
#exec_cmd("rankmirrors -n 10 /etc/pacman.d/mirrorlist.backup > /etc/pacman.d/mirrorlist")

exec_cmd("reflector --latest 200 --country Sweden --country Japan --country India --country \"United Statess\" --country France --country Germany  --age 48 --protocol https --sort rate --save /etc/pacman.d/mirrorlist")
exec_cmd("pacman -Syyu"
    # bootloader
    #+" grub efibootmgr"
    # network manager
    +" networkmanager network-manager-applet"
    # console programs
    +" bash-completion ranger p7zip"
    # file sharing
    +" grsync wget aria2 youtube-dl uget" # filezilla deluge python-cairo
    # xorg and video drivers
    +" xorg-xinit xorg-server xorg-xbacklight "+video_drivers
    # de or wm
    #+" bspwm sxhkd feh lightdm lightdm-gtk-greeter xclip rxvt-unicode pcmanfm xarchiver kupfer"
    #+" gnome"
    +" xfce4 xfce4-goodies xarchiver lightdm lightdm-gtk-greeter"
    # sound server
    +" pulseaudio pulseaudio-alsa alsa-utils alsa-plugins"
    # file systems
    +" dosfstools mtools mtpfs ntfs-3g autofs gvfs"
    # text editors
    +" nano neovim" #emacs code atom
    # web browsers
    +" w3m firefox" #vivaldi chromium
    # audio/video players
    +" mplayer" # vlc spotify
    # fonts
    +" ttf-inconsolata ttf-fira-mono ttf-fira-code ttf-dejavu ttf-roboto noto-fonts ttf-ubuntu-font-family gnu-free-fonts adobe-source-code-pro-fonts ttf-linux-libertine"
    # graphics tools
    +" blender krita inkscape gimp obs-studio"
    # doc tools
    +" zathura zathura-pdf-poppler zathura-djvu zathura-ps" #okular pandoc texlive-most
    # misc
    +" nodejs npm python-pynvim redshift python-virtualenv keepassxc gparted"
    )

# fstrim.timer 
exec_cmd("systemctl enable NetworkManager autofs.service avahi-daemon.service")

#lightdm.service
exec_cmd("systemctl enable lightdm.service")

if bootloader == 'grub':
    exec_cmd("grub-install --target=x86_64-efi --bootloader-id=GRUB --efi-directory=/boot")
    exec_cmd("grub-mkconfig -o /boot/grub/grub.cfg")
if bootloader == 'systemd-boot':
    exec_cmd("bootctl --path=/boot install")
    with open("/boot/loader/loader.conf",'w') as f:
        f.write("default arch\ntimeout 4\nconsole-mode max\neditor no\n")
    root_blkid=os.popen("blkid "+root).read()
    root_uuid=re.search(r".*\ UUID=\"(.*)\"\ TYPE.*",root_blkid).group(1)
    with open("/boot/loader/entries/arch.conf",'w') as f:
        f.write(
            "title   Arch Linux\n"
            +"linux   /vmlinuz-linux\n"
            +"initrd  /"+cpu+"-ucode.img\n"
            +"initrd  /initramfs-linux.img\n"
            +"options root=UUID="+root_uuid+" rw\n")

exec_cmd("exit")
