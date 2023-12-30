#!/bin/bash

read -p "spotify (y)? " spotify;
read -p "discord (y)? " discord;
read -p "i3 (y)? " ithree;
read -p "Frans (y)? " franz;
read -p "Terminal theme (y)? " theme;
if [[ $theme == "y" || $theme == "Y" ]]; then
wget -O gogh https://git.io/vQgMr && chmod +x gogh && ./gogh && rm gogh
fi

############## PREPARING APPS ####################
echo "Adding repositories...";
sudo apt-add-repository -y ppa:yktooo/ppa &> /dev/null;
sudo add-apt-repository -y ppa:webupd8team/atom &> /dev/null;
sudo add-apt-repository -y ppa:snwh/pulp &> /dev/null;
if [[ $grive == "y" || $grive == "Y" ]]; then
sudo add-apt-repository -y ppa:nilarimogard/webupd8 &> /dev/null;
fi

#Spotify
if [[ $spotify == "y" || $spotify == "Y" ]]; then
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys BBEBDCB318AD50EC6865090613B00F1FD2C19886 &> /dev/null
fi

#Final prepare
sudo apt update &> /dev/null;

############## INSTALLING APPS ####################
echo "Installing apps...";
sudo apt install -y git vim zsh fonts-font-awesome fonts-roboto atom dtrx indicator-sound-switcher paper-icon-theme &> /dev/null;
if [[ $grive == "y" || $grive == "Y" ]]; then
sudo apt install -y grive &> /dev/null;
fi

#Spotify
if [[ $spotify == "y" || $spotify == "Y" ]]; then
sudo apt-get install -y spotify-client &> /dev/null
fi

#Franz
if [[ $franz == "y" || $franz == "Y" ]]; then
sudo rm -fr /opt/franz &> /dev/null
sudo rm -fr /usr/share/applications/franz.desktop &> /dev/null
sudo mkdir -p /opt/franz &> /dev/null
wget -qO- https://github.com/meetfranz/franz-app/releases/download/4.0.4/Franz-linux-x64-4.0.4.tgz | sudo tar xvz -C /opt/franz/ &> /dev/null
sudo wget "https://cdn-images-1.medium.com/max/360/1*v86tTomtFZIdqzMNpvwIZw.png" -O /opt/franz/franz-icon.png &> /dev/null
sudo bash -c "cat <<EOF > /usr/share/applications/franz.desktop
[Desktop Entry]
Name=Franz
Comment=
Exec=/opt/franz/Franz
Icon=/opt/franz/franz-icon.png
Terminal=false
Type=Application
Categories=Messaging,Internet
EOF"
fi

#i3
if [[ $ithree == "y" || $ithree == "Y" ]]; then
sudo apt install -y i3;
fi


if [[ $discord == "y" || $discord == "Y" ]]; then
sudo wget -qO- discord.deb https://discordapp.com/api/download?platform=linux&format=deb
sudo dpkg -i discord.deb
rm discord.deb
fi

#Grive
if [[ $grive == "y" || $grive == "Y" ]]; then
cd ~
mkdir $gdir
cd $gdir
grive -a
fi


############## FINALIZING ####################
echo "Upgrading...";
sudo apt upgrade &> /dev/null;
zsh
