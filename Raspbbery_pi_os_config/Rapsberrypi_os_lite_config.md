# File 

## Flashing the image

When flashing the raspberry pi SD card choose the Raspberry pi OS lite as the base os. 
Then when asked to set custom configs, choose yes, after that set the username to `dash` and set the password that you want
Then I recomend that you set up the wifi connection, so that its possible to connect via ssh



## Turn off system services

```bash
sudo systemctl disable keyboard-setup.service
sudo systemctl disable console-setup.service
```

### Turn off bluetooth
```bash
sudo systemctl disable bluetooth.service
sudo systemctl disable hciuart.service
```

### Turn off Swap file (fake ram)

```bash
sudo dphys-swapfile swapoff
sudo dphys-swapfile uninstall
sudo systemctl disable dphys-swapfile.service
sudo apt purge dphys-swapfile -y
```

### Turn off updates
```bash
sudo systemctl disable rpi-eeprom-update.service
```

### Turn off Modem (4G)

```bash
sudo systemctl disable ModemManager.service
sudo apt purge modemmanager -y
```

### Turn off audio manager

```bash
sudo systemctl disable alsa-state.service
```

### Turn off man page updates

```bash
sudo systemctl disable man-db.service
```

### Turn off network wait

```bash
sudo systemctl mask systemd-networkd-wait-online.service
```

## Configure splash screen. 

Add `initramfs initramfs.img` into `/boot/firmware/config.txt` in the top of the file

and 
```txt
hdmi_force_hotplug=1  # Forces HDMI even if no display is detected
hdmi_group=2          # CEA group
hdmi_group=2          # Set to DMT (computer monitor mode)
hdmi_mode=82          # 1080p resolution (change as needed)

framebuffer_width=1024
framebuffer_height=600

boot_delay=0
disable_splash=1
```

Add to `/boot/firmware/cmdline.txt` the same line but with a space between whats in the file and what you are adding 

`logo.nologo loglevel=0 splash silent quiet vt.global_cursor_default=0` 

Now we need to make modifications in the `/boot/firmware/cmdline.txt`, open it with sudo

first remove the `console=tty1`, this is the first step to remove the login prompt, 
but if you want to see the ip addr of the raspberry pi skip this step.

and then add:
`logo.nologo loglevel=0 splash silent quiet vt.global_cursor_default=0` 

now you can save the file.

The second step is to run `sudo systemctl disable getty@tty1.service` to disable the login prompt

Copy the image splash.png to `/boot/firmware/`

Create a new file called splash.txt in /boot/firmware/ `/boot/firmware/splash.txt`

In the file splash.txt add:

```
## Initramfs-Splash
image=splash.png
fullscreen=1
```

Now move initramfs.img to `/boot/firmware`

## Configure WiFi

After adding the first wifi network we can add a second so that the raspberrypi can connect to the meca router

create the file `/etc/NetworkManager/system-connections/DashWifi.nmconnection`

and put this into it: 

``` bash
connection
[connection]
id=DashWifi
uuid=7b255ccc-aa98-4674-9cb7-7831032fad77
type=wifi
interface-name=wlan0

[wifi]
mode=infrastructure
ssid=DashWifi

[wifi-security]
auth-alg=open
key-mgmt=wpa-psk
psk=qwertyui

[ipv4]
method=auto

[ipv6]
addr-gen-mode=default
method=auto

[proxy]
```

then set the right permissions `sudo chmod 600 /etc/NetworkManager/system-connections/DashWifi.nmconnection`

after restarting it should work 

## Configure Python

Install pip: `sudo apt-get install python3-pip`

Now run `echo 'export PIP_BREAK_SYSTEM_PACKAGES=1' >> ~/.bashrc` and `source ~/.bashrc`

Now install the python packages with pip

Now run 
``` bash
sudo apt install python3-kivy
```

Now install gpio package: 
```bash
sudo apt install pigpio python3-pigpio -y && sudo pigpiod
```

Now we need to make pigpiod start on boot, to do this try enabling it `sudo systemctl enable pigpiod.service`

or create a custom service file with this code: 

```bash
[Unit]
Description=Daemon required to control GPIO pins via pigpio
[Service]
ExecStart=/usr/bin/pigpiod -l
ExecStop=/bin/systemctl kill pigpiod
Type=forking
[Install]
WantedBy=multi-user.target
```


## CAN setup

Run `sudo apt update && sudo apt upgrade`  

Add to /boot/firmware/config.txt:
`dtoverlay=mcp251xfd,oscillator=20000000,interrupt=25`

after rebooting, to config the can interface, run:
`sudo ip link set can0 up type can bitrate 500000`

Configure ptyhon code:
```ptyhon
import can

can_bus = can.interface.Bus(interface='socketcan', channel='can0', bitrate=500000)
```

### Setup the python app

Now wee need to get the dash gir repo, you can send it using scp or download it using git.
*if you are using git, remember to run `pip install -r requirements.txt` and 
The whole repo should be in a folder called `dash` in the home dir. 

now send the two service files and run `sudo systemctl enable dashconf.service` 
then change `dashconf.service` with `dash.service`

now you should be able to reboot the raspberry pi and everything should work.
