#!/bin/bash
# from https://github.com/Pantonius/Discord-Update/blob/main/discord-update.sh

url="https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64"
name="Code"
debname="code"
tmpdir=$(mktemp -d /tmp/code-update.XXXXXX)

# navigate to the temp directory
cd $tmpdir

# kill all processes called $name
echo Killing all processes called $name
for KILLPID in `ps ax | grep $name | awk ' { print $1;}'`; do
 kill -9 $KILLPID &> /dev/null
done


echo
echo Getting latest version of $name from $url...
wget -q --show-progress -O $debname $url

# install the deb
echo
echo Installing $debname...
sudo dpkg -i $debname

# removing the temp directory
echo
echo "Cleaning up..."
rm -r $tmpdir

echo Finished;
echo You can now launch $name;