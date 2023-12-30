i=0
while :; do
  if [[ $i -eq 3 ]]; then
    echo "QUITING"
    exit 1
  fi
  if ping -c 1 google.com &> /dev/null; then
    i=0
    sleep 1;
  else
    i=$((i+1))
    echo "Not Working!"
    date
    # sudo ip link set dev usb0 up && sudo dhclient usb0;
    sleep 3;
  fi;
done
