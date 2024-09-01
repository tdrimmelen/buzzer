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

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# install docker
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo usermod -aG docker $USER

echo "Finished. Rebooting in 5 seconds..."
sleep 5s

sudo reboot