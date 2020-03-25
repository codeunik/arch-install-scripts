import re

from config import *

# time zone setup
exec_cmd("ln -sf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime")
exec_cmd("hwclock --systohc")

# localization
with open('/etc/locale.gen', 'a') as f:
    f.write('en_US.UTF-8 UTF-8\nen_US ISO-8859-1\n')
exec_cmd("locale-gen")
with open('/etc/locale.conf', 'a') as f:
    f.write('LANG=en_US.UTF-8\n')

# Network configuration
with open('/etc/hostname', 'a') as f:
    f.write(hostname + '\n')
with open('/etc/hosts', 'a') as f:
    f.write("""
127.0.0.1	localhost
::1		localhost
127.0.1.1	""" + hostname + ".localdomain	" + hostname + '\n')

# Initramfs
exec_cmd("mkinitcpio -P")

# Root password
exec_cmd("passwd")
exec_cmd(
    "useradd -m -g users -G wheel,video,audio,optical,storage,power -s /bin/bash "
    + username)
exec_cmd("passwd " + username)
exec_cmd("EDITOR=nano visudo")

exec_cmd(
    "reflector --latest 200 --country Sweden --country Japan --country India --country \"United States\" --country France --country Germany  --age 48 --protocol https --sort rate --save /etc/pacman.d/mirrorlist"
)
exec_cmd("pacman -Syyu " + " ".join(packages))

exec_cmd("systemctl enable " + " ".join(services))

if bootloader == 'grub':
    exec_cmd(
        "grub-install --target=x86_64-efi --bootloader-id=GRUB --efi-directory=/boot/efi"
    )
    exec_cmd("grub-mkconfig -o /boot/grub/grub.cfg")
if bootloader == 'systemd-boot':
    exec_cmd("bootctl --path=/boot install")
    with open("/boot/loader/loader.conf", 'w') as f:
        f.write("default arch\ntimeout 4\nconsole-mode max\neditor no\n")
    root_blkid = os.popen("blkid " + root).read()
    root_uuid = re.search(r".*UUID=\"(.*?)\"\ .*", root_blkid).group(1)
    with open("/boot/loader/entries/arch.conf", 'w') as f:
        f.write("title   Arch Linux\n" + "linux   /vmlinuz-linux\n" +
                "initrd  /" + cpu + "-ucode.img\n" +
                "initrd  /initramfs-linux.img\n" + "options root=UUID=" +
                root_uuid + " rw\n")

if will_reinstall:
    exec_cmd(
        "mkdir -p /home/partha/pkg/ && cp -r /var/cache/pacman/pkg/* /home/partha/pkg/"
    )

exec_cmd("exit")
