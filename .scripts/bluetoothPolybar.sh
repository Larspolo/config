#!/usr/bin/bash

# Altered from https://github.com/polybar/polybar-scripts/tree/master/polybar-scripts/system-bluetooth-bluetoothctl

FILE=$0

get_device_output() {
    device=$1
    device_info=$(bluetoothctl info "$device")

    # Use alias and add battery percentage to output where available
    device_output=$(echo "$device_info" | grep "Alias" | cut -d ' ' -f 2-)
    device_battery_percent=$(echo "$device_info" | grep "Battery Percentage" | awk -F'[()]' '{print $2}')
    if [ -n "$device_battery_percent" ]; then
        device_output="$device_output ($device_battery_percent%)"
    fi

    echo "$device_output"
}

print_with_onclick() {
    action=$1
    escapedaction="${action//\:/\\\:}"
    string=$2
    escapedstring="${string/\:/\\\:}"
    printf "%%{A1:%s:}%s%%{A}" "$escapedaction" "$escapedstring"
}

list_devices () {
    counter=0
    for device in $1; do
        device_info=$(bluetoothctl info "$device")
        # Add seperator
        if [ $counter -gt 0 ]; then
            printf " | "
        fi

        # Use alias and add battery percentage to output where available
        device_output=$(get_device_output "$device")
        print_with_onclick "$FILE --toggle-device \"$device\"" "$device_output"

        counter=$((counter + 1))
    done
}

bluetooth_print() {
    bluetoothctl | grep --line-buffered 'Device\|#' | while read -r REPLY; do
        if [ "$(systemctl is-active "bluetooth.service")" = "active" ]; then
            devices_paired=$(bluetoothctl devices Paired | grep Device | cut -d ' ' -f 2)
            devices_connected=$(bluetoothctl devices Connected | grep Device | cut -d ' ' -f 2)

            # Print main bluetooth icon, white if off, blue if on, clickable to turn on/off
            if [ $(bluetoothctl show | grep "Powered: yes" | wc -c) -eq 0 ]; then
                print_with_onclick "$FILE --toggle-all" " off"
            # If there is a connected device, only show connected devices
            elif [ -n "$devices_connected" ]; then
                print_with_onclick "$FILE --toggle-all" ""
                printf "  "
                list_devices "$devices_connected"
            else
                print_with_onclick "$FILE --toggle-all" ""
                printf "  "
                list_devices "$devices_paired"
            fi

            printf '\n'
        else
            echo "#2"
        fi
    done
}

bluetooth_toggle_all() {
    if bluetoothctl show | grep -q "Powered: no"; then
        notify-send "Bluetooth" "Turning on"
        bluetoothctl power on >> /dev/null
        sleep 1

        devices_paired=$(bluetoothctl devices Paired | grep Device | cut -d ' ' -f 2)
        echo "$devices_paired" | while read -r line; do
            bluetoothctl connect "$line" >> /dev/null
        done
    else
        notify-send "Bluetooth" "Turning off"
        devices_paired=$(bluetoothctl devices Paired | grep Device | cut -d ' ' -f 2)
        echo "$devices_paired" | while read -r line; do
            bluetoothctl disconnect "$line" >> /dev/null
        done

        bluetoothctl power off >> /dev/null
    fi
}

bluetooth_toggle_device() {
    device=$1
    device_output=$(get_device_output "$device")
    if bluetoothctl info "$device" | grep -q "Connected: yes"; then
        notify-send "Bluetooth" "Disconnecting from $device_output"
        bluetoothctl disconnect "$device" >> /dev/null
    else
        notify-send "Bluetooth" "Connecting to $device_output"
        bluetoothctl connect "$device" >> /dev/null
    fi
}

case "$1" in
    --toggle-all)
        bluetooth_toggle_all
        ;;
    --toggle-device)
        bluetooth_toggle_device "$2"
        ;;
    *)
        bluetooth_print
        ;;
esac