#!/bin/bash

read -p "i3 (y)? " ithree;
read -p "discord (y)? " discord;

echo "Updating packages...";
sudo apt update &> /dev/null;
sudo apt upgrade &> /dev/null;

############## INSTALLING APPS ####################
echo "Installing apps...";
sudo apt install -y curl git vim zsh &> /dev/null;

#i3
if [[ $ithree == "y" || $ithree == "Y" ]]; then
sudo apt install -y i3 maim xclip polybar arandr python3-i3ipc ddccontrol feh libnotify-bin notify-osd msgcat gettext compton maim gnome-terminal-transparency thunar make vim gnome-flashback compton rofi flatpak notify-send
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo 
flatpak install flathub com.github.PintaProject.Pinta
flatpak install flathub com.github.IsmaelMartinez.teams_for_linux
fi

# Extract
sudo apt install -y dtrx

# Backup
sudo apt install -y restic

if [[ $discord == "y" || $discord == "Y" ]]; then
sudo wget -qO- discord.deb https://discordapp.com/api/download?platform=linux&format=deb
sudo dpkg -i discord.deb
rm discord.deb
fi

############## FINALIZING ####################
echo "Upgrading...";
sudo apt upgrade &> /dev/null;
zsh
