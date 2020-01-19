import os

def exec_cmd(cmd):
    print(cmd)
    os.system(cmd)

def aur(pkg):
    exec_cmd("rm -rf /tmp/"+pkg)
    exec_cmd("git clone https://aur.archlinux.org/"+pkg+".git /tmp/"+pkg)
    exec_cmd("cd /tmp/"+pkg+" && makepkg -si")

aur("google-chrome")
#aur("mathpix-snipping-tool")
#aur("polybar")
