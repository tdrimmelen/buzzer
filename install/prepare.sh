#/bin/bash

#Run as normal user
if [ "${USER}" = "root" ] ; then

    echo "Run script as a normal user (should have sudo rights)"
    exit 1

fi

if [ "$1" != "desktop" ] && \
   [ "$1"  != "server" ]  \
   ; then
	
	echo "Missing or unknown option"
	echo "usage: install.sh [desktop|server]"

	exit 1
fi

module=$1

echo "Installing as ${module}..."

if [ "${module}" = "desktop" ] ; then

    sudo apt install -y xserver-xorg
    sudo apt install -y raspberrypi-ui-mods

    # Enable autologin
    sudo systemctl set-default graphical.target
    sudo ln -fs /lib/systemd/system/getty@.service /etc/systemd/system/getty.target.wants/getty@tty1.service
    sudo sh -c 'cat > /etc/systemd/system/getty@tty1.service.d/autologin.conf << EOF
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin pi --noclear %I \$TERM
EOF'
    sudo sed /etc/lightdm/lightdm.conf -i -e "s/^\(#\|\)autologin-user=.*/autologin-user=pi/"


fi

sudo apt install -y curl

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

sudo apt-get install -y libffi-dev libssl-dev
sudo apt-get install -y python3 python3-pip

sudo pip3 -v install docker-compose

sudo usermod -aG docker $USER

echo "Finished. Rebooting in 5 seconds..."
sleep 5s

sudo reboot