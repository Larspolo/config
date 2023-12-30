dhclient

while :
do
    if ping google.com -c 1
    then
        sleep 1
    else
        systemd-resolve --set-dns=8.8.8.8 --interface=enp0s31f6
    fi
done
