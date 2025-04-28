# File 

## Flashing the image

When flashing the raspberry pi SD card choose the Raspberry pi OS lite as the base os. 
Then when asked to set custom configs, choose yes, after that set the username to `dash` and set the password that you want
Then I recomend that you set up the wifi connection, so that its possible to connect via ssh




## Turn off system services

```bash
systemctl disable keyboard-setup.service
systemctl disable console-setup.service
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
hdmi_group=2          # Set to DMT (computer monitor mode)
hdmi_mode=82          # 1080p resolution (change as needed)

framebuffer_width=1920
framebuffer_height=1080

boot_delay=0
disable_splash=1
```

Add to `/boot/firmware/cmdline.txt` the same line but with a space between whats in the file and what you are adding 

`logo.nologo loglevel=0 splash silent quiet vt.global_cursor_default=0` 

Copy the image splash.png to `/boot/firmware/`

Create a new file called splash.txt in /boot/firmware/ `/boot/firmware/splash.txt`

In the file splash.txt add:

```
## Initramfs-Splash
image=splash.png
fullscreen=1
```

Now add initramfs.img to `/boot/firmware`

## Configure Python

Install pip: `sudo apt-get install python3-pip`

Now run `echo 'export PIP_BREAK_SYSTEM_PACKAGES=1' >> ~/.bashrc` and `source ~/.bashrc`

Now install the python packages with pip

Now run 
``` bash
sudo apt install python3-kivy libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libmtdev-dev libgl1-mesa-dev libgles2-mesa-dev libdrm-dev libgbm-dev libudev-dev
```

Now install gpio package: 
```bash
sudo apt install pigpio python3-pigpio -y && sudo pigpiod
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
