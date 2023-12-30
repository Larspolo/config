#!/bin/bash
mouse=$(xinput | grep TouchPad | awk '{match($6,"[0-9]+",a)}END{print a[0]}')
props=$(xinput list-props $mouse | grep -E "Tapping Enabled|Natural Scrolling|Middle Emulation" | tr -dc '(0-9)' | tr '(' '\n')
for i in $props; do
    xinput set-prop $mouse ${i%%\)*} 1
done
