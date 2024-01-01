#!/usr/bin/env sh

# Terminate already running bar instances
killall -q polybar

echo $UID
# Wait until the processes have been shut down
while pgrep -x polybar >/dev/null; do sleep 0.1; done

for m in `polybar -m|tail -2|sed -e 's/:.*$//g'`; do
    MONITOR=$m polybar --reload small --config=$HOME/.config/polybar/config &
done

echo "Bars launched..."

