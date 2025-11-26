1. Download and install Raspberry PI Imager
2. Flashing the OS
    1. In `Device` section, select `Raspberry PI 3` then click `Next`.
    2. In 'OS' setion, select `Raspberry PI OS (other)` then click `Raspberry PI OS Lite (64-bit)`.
    3. Under `Storage` select the `Mass Storage Device USB Device` then click `Next`.
    4. Enter `terra` as Hostname.
    5. In `Localisation`, set `Manila (Philippines)`.
    6. Under `User`, use these credentials:
    ```shell
    Username: terra-rpi-3
    Password: d1gyshvb // Confirm Password
    ```
    7. Conifgure Network in `WiFi` section.
    8. Enable `Raspberry PI Connect`.
    9. Sign up in `https://id.raspberrypi.com/sign-up`
        1. Create auth key and launch Raspberry PI Manager
    10. Write the image.
        1. In case of error in writing caused by storage can't be formatted, try to use `Disk Management` in Windows (Use Gemini for the steps on how to format the storage `micro sd`).
        2. After formatting using the `Disk Management`, rety the `Write` process (make sure to check the `User` and `Wifi` credentials).
    11. After flashing the OS, put the SD Card to RPi.