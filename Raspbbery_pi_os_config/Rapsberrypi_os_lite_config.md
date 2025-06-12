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
autoconnect-priority=5
interface-name=wlan0
timestamp=1749130719

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

also run: `sudo systemctl restart NetworkManager`

after restarting it should work.

## Configure Wifi hotspot

Add a fallback mechanism so that if no usable Wi-Fi connection is established within a minute after boot, the Pi automatically brings up a hotspot. This does not interfere with your existing low-level Wi-Fi setup; it only uses NetworkManager to start the hotspot when truly offline.
1.	Place the fallback script
Decide where to put it; for example:
/home/dash/dash/Raspbbery_pi_os_config/hotspot_if_no_ip.sh
or /usr/local/bin/hotspot_if_no_ip.sh. Adapt ExecStart in the service accordingly.
2. Create the script file
``` bash
sudo nano /home/dash/dash/Raspbbery_pi_os_config/hotspot_if_no_ip.sh
```
Paste this:
``` bash
#!/bin/bash

IFACE="wlan0"
HOTSPOT_CONN="DashHotspot"
TIMEOUT=60

echo "[INFO] Checking for usable Wi-Fi connection on $IFACE..."

for (( i=0; i<TIMEOUT; i++ )); do
    # Get IPv4 address if any
    ip_addr=$(ip -4 addr show "$IFACE" | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
    
    # Check it’s not link-local (169.254.x.x)
    if [[ -n "$ip_addr" && ! "$ip_addr" =~ ^169\.254\. ]]; then
        # Find default gateway for this interface
        gateway=$(ip route | grep "^default" | grep "$IFACE" | awk '{print $3}')
        if [[ -n "$gateway" ]]; then
            # Ping gateway to confirm connectivity
            if ping -c1 -W1 "$gateway" >/dev/null 2>&1; then
                echo "[OK] Connected: IP $ip_addr, gateway $gateway reachable."
                exit 0
            else
                echo "[WAIT] IP assigned ($ip_addr) but gateway $gateway unreachable..."
            fi
        else
            echo "[WAIT] IP assigned ($ip_addr) but no default gateway found..."
        fi
    else
        echo "[WAIT] No valid IP yet..."
    fi
    sleep 1
done

echo "[FAIL] No usable Wi-Fi after $TIMEOUT seconds. Starting hotspot..."
nmcli connection up "$HOTSPOT_CONN"
```

3.	Make the script executable
``` bash
sudo chmod +x /home/dash/dash/Raspbbery_pi_os_config/hotspot_if_no_ip.sh
```

4.	Create the hotspot profile (only once)
If not already created, run:
``` bash
nmcli connection add type wifi ifname wlan0 con-name DashHotspot autoconnect no ssid DashHotspot \
  wifi.mode ap \
  wifi.band bg \
  ipv4.method shared \
  wifi-sec.key-mgmt wpa-psk \
  wifi-sec.psk "dash12345"
```
5. Create systemd service
``` bash
sudo nano /etc/systemd/system/fallback-hotspot.service
```
Paste:
``` bash
[Unit]
Description=Fallback to Hotspot if Wi-Fi not working
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/home/dash/dash/Raspbbery_pi_os_config/hotspot_if_no_ip.sh

[Install]
WantedBy=multi-user.target
```

6.	Enable and reload systemd
``` bash
sudo systemctl daemon-reexec
sudo systemctl enable fallback-hotspot.service
```

You can test immediately:
``` bash
sudo systemctl start fallback-hotspot.service
```

•	If Wi-Fi is already working, you’ll see “[OK] Connected…” and no hotspot startup.
•	If offline, after ~60 seconds it will start DashHotspot.







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

now send the two service files and run `sudo systemctl enable ./dashconf.service` 
then change `./dashconf.service` with `./dash.service`

now you should be able to reboot the raspberry pi and everything should work.
