import os
import sys


def exec_cmd(cmd):
    print(cmd)
    os.system(cmd)


def aur(pkgs):
    download_dir = "~/pkg/"
    exec_cmd("mkdir -p " + download_dir)
    for pkg in pkgs:
        exec_cmd("rm -rf " + download_dir + pkg)
        exec_cmd("git clone https://aur.archlinux.org/" + pkg + ".git " +
                 download_dir + pkg)
        exec_cmd("cd " + download_dir + pkg + " && makepkg -si")


aur(sys.argv[1:])
# google-chrome mathpix-snipping-tool
