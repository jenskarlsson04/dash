## Turn off system services

systemctl disable keyboard-setup.service

systemctl disable console-setup.service

### Turn off bluetooth

sudo systemctl disable bluetooth.service

sudo systemctl disable hciuart.service

### Turn off Swap file (fake ram)

sudo dphys-swapfile swapoff

sudo dphys-swapfile uninstall

sudo systemctl disable dphys-swapfile.service

sudo apt purge dphys-swapfile -y

### Turn off updates

sudo systemctl disable rpi-eeprom-update.service

### Turn off Modem (4G)

sudo systemctl disable ModemManager.service

sudo apt purge modemmanager -y

### Turn off audio manager

sudo systemctl disable alsa-state.service

### Turn off man page updates

sudo systemctl disable man-db.service

# Configure splash screen. 

Add `initramfs initramfs.img` into `/boot/firmware/config.txt` in the top of the file

Add to `/boot/firmware/cmdline.txt` the same line but with a space between whats in the file and what you are adding 

`logo.nologo loglevel=0 splash silent quiet` 

Copy the image splash.png to `/boot/firmware/`

Create a new file called splash.txt in /boot/firmware/ `/boot/firmware/splash.txt`

In the file splash.txt add:

```
## Initramfs-Splash
image=splash.png
fullscreen=1
```

Now add initramfs.img to `/boot/firmware`

# Configure Python

Install pip: `sudo apt-get install python3-pip`

Now run `echo 'export PIP_BREAK_SYSTEM_PACKAGES=1' >> ~/.bashrc` and `source ~/.bashrc`

Now install the python packages with pip

Now run 
``` bash
sudo apt install python3-kivy libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libmtdev-dev libgl1-mesa-dev libgles2-mesa-dev libdrm-dev libgbm-dev libudev-dev
```

# CAN setup

Add to boot/firmware/config.txt:
`dtoverlay=mcp2515-can0, oscillator=16000000, interrupt=25`

config the can interface, run:
`sudo ip link set can0 up type can bitrate 500000`

Configure ptyhon code:
```ptyhon
import can

can_bus = can.interface.Bus(interface='socketcan', channel='can0', bitrate=500000)
```