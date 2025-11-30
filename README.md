# TERRA

This repository contains the source codes and config files for this project.

### Requirements
1. Raspberry PI 3B+
2. Raspbery Pi Imager
3. GitBash for Windows
   - https://git-scm.com/install/windows
   - Download and install `Git for Windows/x64 Setup` on Windows
3. Python3
4. Android Studio
5. Flutter with Dart
6. VSCode (Python Development)
   - Download and install VSCode: https://code.visualstudio.com/
   - Install extension: https://marketplace.visualstudio.com/items?itemName=ms-python.python
6. Sensors
   - DHT11, HD-38

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
    - Sign up in [https://id.raspberrypi.com/sign-up]
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

### Cloning the GitHub Repository (in RPi through SSH Connection)
The following are the shell commands, enter one-by-one.
```shell
# terra-rpi-3@terra:~ $
# Pre-requisites (Package Installation)
sudo apt-get install git # Install git first
sudo apt-get install python3 # Install Python3
```
```shell
# terra-rpi-3@terra:~ $
mkdir ~/dev # Make a directory
cd ~/dev # Go to the dev directory
git clone https://github.com/genedvlpr/project-terra.git # Clone the repository
cd ~/dev/project-terra/
git pull origin master
```
```shell
# Create Python Environment
python3 -m venv ~/dev/project-terra/
# Activate the environment
source ~/dev/project-terra/bin/activate
```
```shell
# Update the package list
sudo apt-get update
# Install Python 3 development headers
sudo apt-get install python3-dev
# Install pip3
sudo apt install python3-pip
# Install the necessary library (sometimes needed for compilation)
pip3 install setuptools
# Install the Adafruit DHT library
pip3 install adafruit-circuitpython-dht
# Install the board library (helps with pin definitions)
pip3 install board
# Install the libgpiod2 library
sudo apt-get install -y python3-pip libgpiod2
# Install the core Blinka library
pip3 install adafruit-blinka
# Example: Install the specific library you need
pip3 install adafruit-circuitpython-dht
# Error fixing
pip install --upgrade --force-reinstall adafruit-blinka
```
- The head directory of the project is on  `~/dev/project-terra/`.

### Coding
The workflow for the development is described as follows:
Note: Make sure Git Bash is already installed on Windows.
1. Clone the Github repository in Windows
`git clone https://github.com/genedvlpr/project-terra.git`
2. The development of python scripts will be in Windows.
3. After creating python scripts (in Windows), push the changes in the repository.
   - Note that all the python scripts must be inside the `project-terra/rpi` directory created by the cloning process.
   - Python codes must be saved as `sensor-name.py` (Python codes as `.py` in small case naming convention)
   - You can push the changes in the repository by these commands.
   ```shell
   git add .
   git commit -m "Message of the commit" # e.g. added dht11 sensor capabilities
   git push origin master
   ```
4. After pushing new codes to the repo, you should access the RPi via ssh as described in the steps earlier and pull the changes from the remote repository.
```shell
# terra-rpi-3@terra:~ $
cd ~/dev/project-terra/
git pull origin master
```
5. Build process below.

### Build
To build the program as a runnable background service, follow the steps below.
```shell
# terra-rpi-3@terra:~ $
cd ~/dev/project-terra/rpi/
chmod +x ~/sensor_project/rpi/main.py
# Edit the Crontab:
crontab -e
# Add the Startup Command: Scroll to the bottom of the file and add the following line.
# This executes your Python script using the correct Python interpreter.
@reboot /usr/bin/python3 /home/terra-rpi-3/dev/project-terra/rpi/main.py &
```
```
The & at the end is crucial—it runs the script in the background, allowing the boot process to complete.
```
```
Save and Exit:If using nano: Press Ctrl + O (to Write Out/Save), then Enter, and then Ctrl + X (to exit).
The console should confirm, "installing new crontab".
```
Test the setup:
```shell
# terra-rpi-3@terra:~/dev/project-terra $
# Reboot the RPi
sudo reboot
# Wait for a few minutes for the Pi to reboot and reconnect to the network.
# SSH back in (ssh terra-rpi-3@<IP_ADDRESS>).
# Check the Running Process: Use the following command to see if your script is active:
pgrep -f dht11_temp_humidity.py # main.py
# If a process ID (PID) number is displayed, your script is running successfully!
```
To run a python script:
```shell
# terra-rpi-3@terra:~/dev/project-terra/rpi/ $
python3 main.py
PROJECT TERRA MAIN MODULE # This is the result
```

### Shutdown the RPi
```shell
# terra-rpi-3@terra:~/dev/project-terra $
sudo shutdown now
# Once the green LED is off and has been off for several seconds, it is safe to unplug the power cable from the Raspberry Pi.
```

### Sample Run Results
![alt text](/assets/image.png)