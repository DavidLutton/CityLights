set -x

cd ~

# From https://github.com/linusg/rpi-backlight 
# Set permissions for users to control backlight
echo 'SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"' | sudo tee -a /etc/udev/rules.d/backlight-permissions.rules

# Get software
git clone https://github.com/DavidLutton/CityLights

cd ~/CityLights/

python3 venv_create.py 
./.venv/bin/python3 venv_install.py

# ./.venv/bin/python lights_pysimplegui.py 

# Copy in the .desktop file to autostart the software 
sudo cp lights_ui.desktop /etc/xdg/autostart/lights_ui.desktop
sudo chown root:root      /etc/xdg/autostart/lights_ui.desktop
sudo chmod 0644           /etc/xdg/autostart/lights_ui.desktop

sudo cp lights_ui.desktop ~/Desktop/lights_ui.desktop

# Sets the lcd rotation to match the enclosure
grep -qxF 'lcd_rotate=2' /boot/config.txt || echo 'lcd_rotate=2' | sudo tee -a /boot/config.txt

echo 'Manual setup of the taskbar:'
echo 'Using a mouse, right click on the taskbar and click on panel settings'
echo 'Click on the "Advanced" tab and enable "Minimise panel when not in use"'
echo 'And set the "Size when minimised" to 0'
echo 'Click "Close"'

echo 'Reboot'