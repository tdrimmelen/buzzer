# Shotclock / scoreboard buzzer

Project that plays a sound when a shotclock / scoreboard has counted down to 0.

## Install

**Run as pi user!**

### Docker

Install the prerequisites (docker). Run the following commands as the `pi` user.

``` bash
wget https://raw.githubusercontent.com/tdrimmelen/buzzer/master/install/prepare.sh

source ./prepare.sh server
```

The Pi is automatically rebooted when the installation completes.

### Buzzer

Install the buzzer software. Run the following commands as the `pi` user.

``` bash
wget https://raw.githubusercontent.com/tdrimmelen/buzzer/master/install/install.sh

source ./install.sh
```

The Pi is automatically rebooted when the installation completes.

## Configure

The configuration default is that the buzzer runs on the same Pi as the shotclock. In the following situations, additional configuration is needed:

- Buzzing for scoreboards
- Buzzing for shotclock / scoreboard running on another Pi
- Using the shotclock / scorebaord test interface

Below you find the needed changes. To effectuate the change, you need to restart the buzzer daemon:

``` bash
sudo systemctl restart buzzer
```

### Time offset

If the buzzer chimes too early, you can set an offset between the time the device reaches 0 and time the buzzer chimes.

Open `~/buzzer/docker/docker-compose.yaml` with a text editor (nano, vim)

Edit the line. The value is in seconds:

``` yaml
      - "BUZZER_OFFSET=0.0"
```

Typically, the value should be set to 1 second when it is off.

### scoreboards

Open `~/buzzer/docker/docker-compose.yaml` with a text editor (nano, vim)

Replace the line:

``` yaml
      - "BUZZER_CLOCKURL=http://localhost/shotclock/time"`
```

by:

``` yaml
      - "BUZZER_CLOCKURL=http://localhost/scoreboard/time"`
```

### Run on a different Pi

Open `~/buzzer/docker/docker-compose.yaml` with a text editor (nano, vim)

Replace the line:


``` yaml
      - "BUZZER_CLOCKURL=http://localhost/shotclock/time"`
```

by:

``` yaml
      - "BUZZER_CLOCKURL=http://<IP of Pi running shotclock>/shotclock/time"`
```

### Test interface

Open `~/buzzer/docker/docker-compose.yaml` with a text editor (nano, vim)

Replace the line:


``` yaml
      - "BUZZER_CLOCKURL=http://localhost/shotclock/time"`
```

by:

``` yaml
      - "BUZZER_CLOCKURL=http://localhost/shotclock/test/time"`
```

## Notes

### List output

Output can be listed with:

``` bash
cd ~\buzzer\docker
docker compose logs
```

### Check status service

``` bash
sudo systemctl status buzzer
```

### Set logging level

Open `~/buzzer/docker/docker-compose.yaml` with a text editor (nano, vim)

Edit the line:


``` yaml
      - "LOGLEVEL=INFO"
```

Replace `INFO` by `DEBUG`

### Sound

run `alsamixer` to configure sound level

### FAQ

Q: I get the following error `Error: aplay: main:828: audio open error: No such file or directory`

A:
Most likely the device number is non existing

Check `/etc/asound.conf`
