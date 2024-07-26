from os import system
import time

partition = str(input("Ввидите ваш диск"))

print("Монтирование и форматирование ваших разделов")
system(f"mkfs.fat -F32 /dev/{partition}p1")
system(f"mkfs.ext4 -L boot /dev/{partition}p2")
system(f"mkswap -L swap /dev/{partition}p3")
system(f"swapon /dev/{partition}p3")
system(f"mkfs.btrfs -L arch /dev/{partition}p4 -f")
system(f"mount /dev/{partition}p4 /mnt")
system("btrfs su cr /mnt/@")
system("btrfs su cr /mnt/@var")
system("btrfs su cr /mnt/@home")
system("btrfs su cr /mnt/@snapshots")
system("umount /mnt")
system(f"mount -o noatime,compress=lzo,space_cache=v2,ssd,subvol=@ /dev/{partition} /mnt")
system("mkdir -p /mnt/{home,boot,var,.snapshots}")
system(f"mount -o noatime,compress=lzo,space_cache=v2,ssd,subvol=@var /dev/{partition} /mnt/var")
system(f"mount -o noatime,compress=lzo,space_cache=v2,ssd,subvol=@home /dev/{partition} /mnt/home")
system(f"mount -o noatime,compress=lzo,space_cache=v2,ssd,subvol=@snapshots /dev/{partition} /mnt/.snapshots")
system(f"mount /dev/{partition}p2 /mnt/boot")
system("mkdir /mnt/boot/efi")
system(f"mount /dev/{partition}p2 /mnt/boot/efi")

choice = int(input( "1 - amd,"
                    "2 - intel - "))

if choice == 1:
    system("pacstrap /mnt base base-devel linux-lts linux-lts-headers linux-firmware amd-ucode nano")
elif choice == 2:
    system("pacstrap /mnt base base-devel linux linux-headers linux-firmware intel-ucode nano")
else:
    print("Ошибка")

system("genfstab -pU /mnt >> /mnt/etc/fstab")
system("arch-chroot /mnt")
print("Поставьте пароль для рута")
system("passwd")
print("Поставьте пароль для компьютера")
time.sleep(3)
system("nano /etc/hostname")
system("ln -sf /usr/share/zoneinfo/Asia/Almaty /etc/localtime")
print("Раскоментируйте en_US.UTF8 и ru_RU.UTF8")
time.sleep(3)
system("nano /etc/locale.gen")
system("locale-gen")

with open("/etc/vconsole.conf", "w") as f:
    f.write("KEYMAP=ru"
            "FONT=cyr-sun16")
with open("/etc/locale.conf", "w") as f:
    f.write('LANG="ru_RU.UTF-8"')

system("pacman-key --init")
system("pacman-key --populate archlinux")
with open("/etc/pacman.conf", "w") as f:
    f.write('#'
'# /etc/pacman.conf'
'#'
'# See the pacman.conf(5) manpage for option and repository directives'

'#'
'# GENERAL OPTIONS'
'#'
'[options]'
'# The following paths are commented out with their default values listed.'
'# If you wish to use different paths, uncomment and update the paths.'
'#RootDir     = /'
'#DBPath      = /var/lib/pacman/'
'#CacheDir    = /var/cache/pacman/pkg/'
'#LogFile     = /var/log/pacman.log'
'#GPGDir      = /etc/pacman.d/gnupg/'
'#HookDir     = /etc/pacman.d/hooks/'
'HoldPkg     = pacman glibc'
'#XferCommand = /usr/bin/curl -L -C - -f -o %o %u'
'#XferCommand = /usr/bin/wget --passive-ftp -c -O %o %u'
'#CleanMethod = KeepInstalled'
'Architecture = auto'

'# Pacman won`t upgrade packages listed in IgnorePkg and members of IgnoreGroup'
'#IgnorePkg   ='
'#IgnoreGroup ='

'#NoUpgrade   ='
'#NoExtract   ='

'# Misc options'
'#UseSyslog'
'#Color'
'#NoProgressBar'
'CheckSpace'
'#VerbosePkgLists'
'ParallelDownloads = 10'

'# By default, pacman accepts packages signed by keys that its local keyring'
'# trusts (see pacman-key and its man page), as well as unsigned packages.'
'SigLevel    = Required DatabaseOptional'
'LocalFileSigLevel = Optional'
'#RemoteFileSigLevel = Required'

'# NOTE: You must run `pacman-key --init` before first using pacman; the local'
'# keyring can then be populated with the keys of all official Arch Linux'
'# packagers with `pacman-key --populate archlinux`.'

'#'
'# REPOSITORIES'
'#   - can be defined here or included from another file'
'#   - pacman will search repositories in the order defined here'
'#   - local/custom mirrors can be added here or in separate files'
'#   - repositories listed first will take precedence when packages'
'#     have identical names, regardless of version number'
'#   - URLs will have $repo replaced by the name of the current repo'
'#   - URLs will have $arch replaced by the name of the architecture'
'#'
'# Repository entries are of the format:'
'#       [repo-name]'
'#       Server = ServerName'
'#       Include = IncludePath'
'#'
'# The header [repo-name] is crucial - it must be present and'
'# uncommented to enable the repo.'
'#'

'# The testing repositories are disabled by default. To enable, uncomment the'
'# repo name header and Include lines. You can add preferred servers immediately'
'# after the header, and they will be used before the default mirrors.'

'#[core-testing]'
'#Include = /etc/pacman.d/mirrorlist'

'[core]'
'Include = /etc/pacman.d/mirrorlist'

'#[extra-testing]'
'#Include = /etc/pacman.d/mirrorlist'

'[extra]'
'Include = /etc/pacman.d/mirrorlist'

'# If you want to run 32 bit applications on your x86_64 system,'
'# enable the multilib repositories as required here.'

'#[multilib-testing]'
'#Include = /etc/pacman.d/mirrorlist'

'[multilib]'
'Include = /etc/pacman.d/mirrorlist'

'# An example of a custom package repository.  See the pacman manpage for'
'# tips on creating your own repositories.'
'#[custom]'
'#SigLevel = Optional TrustAll'
'#Server = file:///home/custompkgs')

system("pacman -Sy")
system("pacman -S openssh arch-install-scripts networkmanager git wget btop fastfetch xdg-user-dirs pacman-contrib ntfs-3g")
system("mkinitcpio -p linux-lts")

with open("/etc/sudoers", "w") as f:
    f.write("root ALL=(ALL:ALL) ALL"

"## Uncomment to allow members of group wheel to execute any command"
"%wheel ALL=(ALL:ALL) ALL"

"## Same thing without a password"
"# %wheel ALL=(ALL:ALL) NOPASSWD: ALL"

"## Uncomment to allow members of group sudo to execute any command"
"# %sudo	ALL=(ALL:ALL) ALL"

"## Uncomment to allow any user to run sudo if they know the password"
"## of the user they are running the command as (root by default)."
"# Defaults targetpw  # Ask for the password of the target user"
"# ALL ALL=(ALL:ALL) ALL  # WARNING: only use this together with 'Defaults targetpw'"

"## Read drop-in files from /etc/sudoers.d"
"@includedir /etc/sudoers.d")

user_name = str(input("Ввидите ваше имя: "))
system(f"useradd -mg users -G wheel {user_name}")
system(f"passwd {user_name}")
system("systemctl enable NetworkManager.service")
time.sleep(2)
system("pacman -S grub efibootmgr grub-btrfs os-prober")
system("grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=Arch")
system("grub-mkconfig -o /boot/grub/grub.cfg")

choice_2 = int(input("1 - нвидия + амд,"
                     "2 - нвидия + интел - "))
if choice_2 == 1:
    system("pacman -S nvidia-utils lib32-nvidia-utils nvidia-settings nvidia-dkms")
    system("pacman -S lib32-mesa vulkan-radeon lib32-vulkan-radeon vulkan-icd-loader lib32-vulkan-icd-loader")
elif choice_2 == 2:
    system("pacman -S xf86-video-intel")
    system("pacman -S nvidia-utils lib32-nvidia-utils nvidia-settings nvidia-dkms")
else:
    pass

system("pacman -S sddm dolphin konsole kate plasma plasma-nm plasma-pa powerdevil gwenview power-profiles-daemon")
system("systemctl enable sddm")
system("exit")
system("umount -R /mnt")
system("reboot")
