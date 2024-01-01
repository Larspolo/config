#!/bin/sh

# Altered from https://github.com/polybar/polybar-scripts/tree/master/polybar-scripts/system-bluetooth-bluetoothctl

bluetooth_print() {
    bluetoothctl | grep --line-buffered 'Device\|#' | while read -r REPLY; do
        if [ "$(systemctl is-active "bluetooth.service")" = "active" ]; then
            devices_paired=$(bluetoothctl devices Paired | grep Device | cut -d ' ' -f 2)
            counter=0
            if [ $(bluetoothctl show | grep "Powered: yes" | wc -c) -eq 0 ]; then
                printf "%%{F#c5c8c6}"
            else
                printf "%%{F#81a2be}"
            fi
            for device in $devices_paired; do
                device_info=$(bluetoothctl info "$device")

                if echo "$device_info" | grep -q "Connected: yes"; then
                    device_output=$(echo "$device_info" | grep "Alias" | cut -d ' ' -f 2-)
                    device_battery_percent=$(echo "$device_info" | grep "Battery Percentage" | awk -F'[()]' '{print $2}')

                    if [ -n "$device_battery_percent" ]; then
                        device_output="$device_output $device_battery_percent%"
                    fi

                    if [ $counter -gt 0 ]; then
                        printf ", %s" "$device_output"
                    else
                        printf " %s" "$device_output"
                    fi

                    counter=$((counter + 1))
                fi
            done

            printf '\n'
        else
            echo "#2"
        fi
    done
}

bluetooth_toggle() {
    if bluetoothctl show | grep -q "Powered: no"; then
        bluetoothctl power on >> /dev/null
        sleep 1

        devices_paired=$(bluetoothctl devices Paired | grep Device | cut -d ' ' -f 2)
        echo "$devices_paired" | while read -r line; do
            bluetoothctl connect "$line" >> /dev/null
        done
    else
        devices_paired=$(bluetoothctl devices Paired | grep Device | cut -d ' ' -f 2)
        echo "$devices_paired" | while read -r line; do
            bluetoothctl disconnect "$line" >> /dev/null
        done

        bluetoothctl power off >> /dev/null
    fi
}

case "$1" in
    --toggle)
        bluetooth_toggle
        ;;
    *)
        bluetooth_print
        ;;
esac