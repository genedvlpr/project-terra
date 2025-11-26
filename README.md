# TERRA

This repository contains the source codes and config files for this project.

### Requirements
1. Raspberry PI 3B+
2. Raspbery Pi Imager
3. Python3
4. Android Studio
5. Flutter with Dart
6. Sensors
   - DHT11

### Flashing the OS

1. Download and install Raspberry PI Imager
2. Flashing the OS
    - In `Device` section, select `Raspberry PI 3` then click `Next`.
    - In `OS` setion, select `Raspberry PI OS (other)` then click `Raspberry PI OS Lite (64-bit)`.
    - Under `Storage` select the `Mass Storage Device USB Device` then click `Next`.
    - Enter `terra` as Hostname.
    - In `Localisation`, set `Manila (Philippines)`.
    - Under `User`, use these credentials:
    ```shell
    Username: terra-rpi-3
    Password: d1gyshvb // Confirm Password
    ```
    - Conifgure Network in `WiFi` section.
    - Enable `Raspberry PI Connect`.
    - Sign up in `https://id.raspberrypi.com/sign-up`
        + Create auth key and launch Raspberry PI Manager
    - Write the image.
        + In case of error in writing caused by storage can't be formatted, try to use `Disk Management` in Windows (Use Gemini for the steps on how to format the storage `micro sd`).
        + After formatting using the `Disk Management`, retry the `Write` process (make sure to check the `User` and `Wifi` credentials).
    - Once completed, click `Finish`.
    - Eject the sd card.
    - After flashing the OS, don't put the SD Card to RPi yetm follow the `Configuration` step.

### Configuration
- Find the config.txt in the newly flashed image (in File Explorer, open `bootfs` drive)
- Open `config.txt` and add these lines at the end of the file.
```
hdmi_force_hotplug=1
hdmi_safe=1  # Use this for maximum compatibility (low resolution)
```
- Once the file is already saved, eject the sd card and put it back to the RPi.

### First Boot
- Connect an external monitor to see what's happening in the initial boot setup.
- Wait a few minutes until you see these:
```
Debian GNU/Linux 13 terra tty1
...
My IP Address is (e.g. 192.168.254.109, if you see something like 127.0.1.1, it means its not connected with the wifi)
```

### SSH Connection
- To confirm that you can connect with the RPi through SSH, open `cmd` in Windows.
- In the command prompt, type this:
```shell
ssh terra-rpi-3@192.168.254.109
```
- Change with the actual IP Address.
- The result should be something like this:
```
The authenticity of host '192.168.254.109 (192.168.254.109)' can't be established.
ED25519 key fingerprint is SHA256:EmwlcPLxzIBy5mrwLG8gNOyTiGz+SNHj4MMmPZ3m0Mg.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? (yes)
```
- If asked for the password, enter the password `d1gyshvb`
```
terra-rpi-3@192.168.254.109's password: d1gyshvb
```
- If the connection is successful, you can now see these:
```
Linux terra 6.12.47+rpt-rpi-v8 #1 SMP PREEMPT Debian 1:6.12.47-1+rpt1 (2025-09-16) aarch64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
terra-rpi-3@terra:~ $
```