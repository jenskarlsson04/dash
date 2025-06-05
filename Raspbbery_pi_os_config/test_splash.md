The intermittent behavior you're describing with the splashscreen on your Raspberry Pi 3 suggests a race condition or timing issue between:

1. **The HDMI output becoming active**, and
2. **The splashscreen image being displayed by the initramfs**.

Here are the most common causes and potential fixes:

---

### 🧭 Likely Causes

#### 1. **HDMI Initialization Delay**

* Some HDMI screens (especially cheap or older ones) take longer to initialize after getting power.
* If the framebuffer tries to draw the splashscreen **before** the HDMI link is ready, the screen may stay blue or flash briefly.

#### 2. **Display resolution mismatch or EDID fallback**

* The Pi might not be getting a valid EDID from the display during boot, leading to resolution negotiation issues.
* This might cause the framebuffer to misconfigure, which could result in no visible splash.

#### 3. **Splashscreen timing**

* If your splashscreen is displayed via a script in `initramfs` or early boot, and the script exits too quickly (e.g. systemd boot completes fast), the image may flash or not appear at all.

---

### ✅ Fixes & Workarounds

#### 1. **Force HDMI Output Early**

In `/boot/config.txt`, add:

```ini
# Force HDMI even if no HDMI monitor is detected
hdmi_force_hotplug=1

# Set a specific resolution (adjust to match your display)
hdmi_group=2
hdmi_mode=87
hdmi_cvt=1024 600 60 6 0 0 0  # Example for 1024x600 60Hz

# Prevent screen blanking (just in case)
disable_splash=1
consoleblank=0
```

#### 2. **Delay the Splashscreen in Initramfs**

If you're using a custom initramfs script to show the splashscreen, add a short delay before or after it runs:

```sh
sleep 1  # Give HDMI time to initialize
```

Also ensure you're writing to the correct framebuffer, e.g.:

```sh
cat /etc/splashscreen.ppm > /dev/fb0
```

Make sure `/dev/fb0` is actually the HDMI framebuffer and not one from another display driver like a PiTFT.

#### 3. **Use `fbset` to Force Framebuffer Mode**

In early boot (in initramfs), explicitly set the framebuffer mode:

```sh
fbset -fb /dev/fb0 -xres 1024 -yres 600
```

Install `fbset` in your initramfs or base image if it's not available.

#### 4. **Check for Splashscreen Size Compatibility**

Make sure your image (e.g. `splash.ppm`) exactly matches the screen resolution (e.g. 1024x600). Otherwise, the image might not display properly.

---

### 🧪 Debug Tips

1. Add `boot_delay=1` to `/boot/config.txt` to introduce a slight delay after GPU firmware finishes.
2. Capture serial output to see if anything is failing silently.
3. Temporarily add `console=tty1` back to `cmdline.txt` to get visual feedback during boot (remove later when testing is done).

---

Let me know what your splashscreen setup script looks like in the initramfs, and I can help you fine-tune the timing or commands.
