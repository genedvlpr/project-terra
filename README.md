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
    - In 'OS' setion, select `Raspberry PI OS (other)` then click `Raspberry PI OS Lite (64-bit)`.
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
        + After formatting using the `Disk Management`, rety the `Write` process (make sure to check the `User` and `Wifi` credentials).
    - After flashing the OS, put the SD Card to RPi.