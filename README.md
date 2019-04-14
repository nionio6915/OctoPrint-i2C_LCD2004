# OctoPrint-i2C_LCD2004

This plug-in allows you to control a 20x4 LCD display (HD44780 connected via PCF8574 backpack to I2C) to display the octoprint status.

This plugin is a remix of the originals Lcd1602 by n3bojs4, and Kunsi's PiATX breakout and HD444780 analog plugin. 

Updated and expanded PiATX breakout by Duckle - git.io/PiATX 

It is useful for people who have a printer without a display, or to add a second display to a printer to show extended information beyond the contoller's display.

It indicates on which port the printer is connected, the progress of printing. It also displays the remaining print time (thanks to a simple method).

This plugin has to evolve:

- add options in the interface
- new version for oled displays :)

nionio EDIT: attempt to change to 2004 LCD with I2C backpack, for use with PiATX hat, git.io/PiATX. 
edits to __init__.py

raspi appears to need some packages installed -
https://github.com/dbrgn/RPLCD ->  
     git clone https://github.com/dbrgn/RPLCD
     cd RPLCD
     sudo python setup.py install

sudo apt install python-smbus
sudo pip install smbus2
sudo pip install fake_rpi

recommended additional package of i2ctools for raspi -
sudo apt-get install ic2tools

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

 original plugin repo at-   https://github.com/nionio6915/octoprint-i2C_LCD2004/archive/master.zip

**MANUAL INSTALL:**

clone the repo :

`https://github.com/nionio6915/octoprint-i2C_LCD2004`

install :
verify directory at install!

`cd octoprint-LCD2004 && python setup.py install`

## Configuration

Nothing to do for the moment :D
