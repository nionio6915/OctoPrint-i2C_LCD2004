# coding=utf-8

"""
  i2C-LCD2004 Plugin for Octoprint
"""

from __future__ import absolute_import
from octoprint.printer.estimation import PrintTimeEstimator
import octoprint.plugin
import octoprint.events
from RPLCD.i2c import CharLCD
import time
import datetime
import os
import sys
from fake_rpi import printf
import fake_rpi


class i2C_LCD2004Plugin(octoprint.plugin.StartupPlugin,
                    octoprint.plugin.EventHandlerPlugin,
                    octoprint.plugin.ProgressPlugin):

  def __init__(self):
    if (os.getenv('i2C-LCD2004_DOCKER')):
      print('We are running in test environnement, no i2c device attached.')
      try:
        print('Loading fake_rpi instead of smbus2')
        sys.modules['smbus2'] = fake_rpi.smbus
        self.mylcd = fake_rpi.smbus.SMBus(1)
      except:
        print('Cannot load fake_rpi !')
    else:
      self.mylcd = CharLCD(i2c_expander='PCF8574', address=0x27, cols=20, rows=4, backlight_enabled=True, charmap='A02')

      # nionion edit
      # self.mylcd = CharLCD(i2c_expander='PCF8574', address=0x27, cols=16, rows=2, backlight_enabled=True, charmap='A00')
      # test change for upload
      #
      #lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
      #        cols=20, rows=4, dotsize=8,
      #        charmap='A02',
      #        auto_linebreaks=True,
      #        backlight_enabled=True)

	# create block for progress bar
      self.block = bytearray(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF')
      self.block.append(255)
      self.mylcd.create_char(1,self.block)
    
    # init vars
    self.start_date = 0

    # create block for progress bar
    #self.mylcd.create_char(1,self.block)

  def JobIsDone(self,lcd):

    # create final anim
    self.birdy = [ '^_-' , '^_^', '-_^' , '^_^', '0_0', '-_-', '^_-', '^_^','@_@','*_*','$_$','<_<','>_>']

    for pos in range(0,13):
      lcd.cursor_pos = (1,pos)
      lcd.write_string(self.birdy[pos])
      time.sleep(0.5)
      lcd.clear()
    lcd.write_string('Job is Done    \,,/(^_^)\,,/')

      
  def on_after_startup(self):
    mylcd = self.mylcd
    self._logger.info("plugin initialized !")

  
  def on_print_progress(self,storage,path,progress):
    mylcd = self.mylcd
    percent = int(progress/6.25)+1
    completed = '\x01'*percent
    mylcd.clear()
    mylcd.write_string('Completed: '+str(progress)+'%')
    mylcd.cursor_pos = (1,0)
    mylcd.write_string(completed)

    if progress==1 :
      self.start_date=time.time()
  
    if progress>10 and progress<100:
      now=time.time()
      elapsed=now-self.start_date
      average=elapsed/(progress-1)
      remaining=int((100-progress)*average)
      remaining=str(datetime.timedelta(seconds=remaining))
      mylcd.cursor_pos = (1,3)
      mylcd.write_string(remaining)

    if progress==100 :
      self.JobIsDone(mylcd)



  def on_event(self,event,payload):
    mylcd = self.mylcd
      
    if event in "Connected":
      mylcd.clear()
      mylcd.write_string('Connected to:')
      mylcd.cursor_pos = (1,0)
      mylcd.write_string(payload["port"])

    if event in "Shutdown":
      mylcd.clear()
      mylcd.write_string('Bye bye ^_^')
      time.sleep(1)
      mylcd._set_backlight_enabled(False)
      mylcd.close()
    
    
    if event in "PrinterStateChanged":
      
      if payload["state_string"] in "Offline":
        mylcd.clear()
        mylcd.write_string('Octoprint is not connected')
        time.sleep(2)
        mylcd.clear()
        mylcd.write_string('saving a polar bear, eco mode ON')
        time.sleep(5)
        mylcd._set_backlight_enabled(False)
      
      if payload["state_string"] in "Operational":
        mylcd._set_backlight_enabled(True)
        mylcd.clear()
        mylcd.write_string('Printer is       Operational')
      
      if payload["state_string"] in "Cancelling":
        mylcd.clear()
        mylcd.write_string('Printer  is Cancelling job') 
        time.sleep(0.2)
      
      if payload["state_string"] in "PrintCancelled":
        mylcd.clear()
        time.sleep(0.5)
        mylcd.write_string(' Job has been Cancelled (0_0) ' ) 
        time.sleep(2)
      
      if payload["state_string"] in "Paused":
        mylcd.clear()
        time.sleep(0.5)
        mylcd.write_string('Printer is  Paused') 

      if payload["state_string"] in "Resuming":
        mylcd.clear()
        mylcd.write_string('Printer is Resuming its job') 
        time.sleep(0.2)

  def get_update_information(self):
      return dict(
          i2C-LCD2004Plugin=dict(
              displayName="i2C-LCD2004 display",
              displayVersion=self._plugin_version,

              type="github_release",
              current=self._plugin_version,
              user="nionio6915",
              repo="OctoPrint-i2C_LCD2004",

              pip="https://github.com/nionio6915/octoprint-i2C_LCD2004/archive/{target}.zip"
          )
      )

__plugin_name__ = "i2C-LCD2004 display"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = i2C-LCD2004()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
