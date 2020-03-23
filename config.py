efi = "/dev/sda1"
root = "/dev/sda2"
home = "/dev/sda3"
swap = "/dev/sda4"
swapfile = False

#cpu = "intel"
cpu = "amd"

bootloader = "systemd-boot"
#bootloader = "grub"

#video_drivers = ["xf86-video-intel", "xf86-video-ati"]
video_drivers = ["nvidia", "nvidia-settings", "nvidia-utils"]

hostname = 'jarvis'
username = 'partha'

pkgs = [
    # bootloader
    # ==========
    # "grub",
    # "efibootmgr",

    # network manager
    # ===============
    # "networkmanager",
    # "network-manager-applet",

    # console programs
    # ================
    "bash-completion",
    "ranger",
    "p7zip",

    # file sharing
    # ==================================
    "grsync",
    "wget",
    "aria2",
    "youtube-dl",
    "uget",
    "filezilla",
    # "deluge",
    # "python-cairo",

    # xorg
    # ====
    "xorg-xinit",
    "xorg-server",
    "xorg-xbacklight",

    # window managers
    # ===============
    # BSPWM
    # =====
    # "bspwm",
    # "sxhkd",
    # "feh",
    # "lightdm",
    # "lightdm-gtk-greeter",
    # "xclip",
    # "rxvt-unicode",
    # "pcmanfm",
    # "xarchiver",
    # "kupfer",

    # desktop environments
    # ====================
    # GNOME
    # =====
    "gnome",
    "gnome-extra",
    # XFCE
    # ====
    # "xfce4",
    # "xfce4-goodies",
    # "xarchiver",
    # "lightdm",
    # "lightdm-gtk-greeter",

    # sound server
    # ============
    "pulseaudio",
    "pulseaudio-alsa",
    "alsa-utils",
    "alsa-plugins",

    # file systems
    # ============
    "dosfstools",
    "mtools",
    "mtpfs",
    "ntfs-3g",
    "autofs",
    "gvfs",

    # text editors
    # ============
    "nano",
    "neovim",
    "emacs",
    # "code",
    # "atom",

    # web browsers
    # ============
    "w3m",
    "firefox",
    # "vivaldi",
    # "chromium",

    # audio/video players
    # ===================
    "mplayer",
    "vlc",

    # fonts
    # =====
    # "ttf-inconsolata", "ttf-fira-mono", "ttf-fira-code", "ttf-dejavu",
    # "ttf-roboto", "noto-fonts", "ttf-ubuntu-font-family", "gnu-free-fonts",
    # "adobe-source-code-pro-fonts", "ttf-linux-libertine",

    # graphics tools
    # ==============
    "inkscape",
    "gimp",
    # "blender",
    # "krita",
    # "obs-studio",

    # doc tools
    # =========
    "texlive-most",
    # "pandoc",
    # "zathura", "zathura-pdf-poppler", "zathura-djvu", "zathura-ps",
    # "okular",
    # "evince",

    # misc
    # ====
    "nodejs",
    "npm",
    "python-pynvim",
    "redshift",
    "python-virtualenv",
    "keepassxc",
    "gparted"
] + video_drivers
