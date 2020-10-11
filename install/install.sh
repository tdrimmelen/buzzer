#/bin/bash

#Run as normal user
if [ "${USER}" = "root" ] ; then

    echo "Run script as a normal user (should have sudo rights)"
    exit 1
    
fi

module='buzzer'
sw=${module}


sudo apt-get install -y git

git config --global user.name "tdrimmelen"
git clone https://github.com/tdrimmelen/buzzer.git

cd buzzer/docker/
docker login
docker-compose pull

cd ${HOME}
sudo cp ${module}/conf/${sw}.service /etc/systemd/system/
sudo systemctl enable ${sw}

echo "Finished. Rebooting in 5 seconds..."
sleep 5s

sudo reboot