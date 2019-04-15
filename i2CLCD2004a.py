# coding=utf-8

from __future__ import absolute_import
from octoprint.printer.estimation import PrintTimeEstimator
import octoprint.plugin
import octoprint.events
from RPLCD.i2c import CharLCD
import time
import datetime
import os
import sys
# from fake_rpi import printf
# import fake_rpi


class i2CLCD2004Plugin(octoprint.plugin.StartupPlugin,
                    octoprint.plugin.SettingsPlugin,
                    octoprint.printer.PrinterCallback,
                    octoprint.plugin.EventHandlerPlugin,
                    octoprint.plugin.ProgressPlugin):

  def __init__(self):
      self.mylcd = CharLCD('PCF8574', 0x27, port=1, cols=20, rows=4, backlight_enabled=True, charmap='A02')

      # self.mylcd = CharLCD(i2c_expander='PCF8574', address=0x27, cols=20, rows=4, backlight_enabled=True, charmap='A00')
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
      self.mylcd.create_char(1,self.block)

  def JobIsDone(self,lcd):

    # create final anim
    self.birdy = [ '^_-' , '^_^', '-_^' , '^_^', '0_0', '-_-', '^_-', '^_^','@_@','*_*','$_$','<_<','>_>']

    for pos in range(0,19):
      lcd.cursor_pos = (1,pos)
      lcd.write_string(self.birdy[pos])
      time.sleep(0.5)
      lcd.clear()
      lcd.write_string('Job is Done    \,,/(^_^)\,,/')


  def on_startup(self):
      mylcd = self.mylcd
      self._logger.info("i2C LCD2004 plugin started !")
      mylcd.write_string('i2CLCD2004 plugin started')
      
  def on_after_startup(self):
      mylcd = self.mylcd
      self._logger.info("i2C LCD2004 plugin initialized !")
      mylcd.write_string('Octoprint Starting Up')
      mylcd.write_string('Hello  World!\r\n')
      mylcd.write_string('Display i2C LCD2004 Initialized')

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
      time.sleep(5)
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


__plugin_name__ = "i2CLCD2004"
__plugin_version__ = "0.1.0"
__plugin_description__ = "i2CLCD2004 Plugin"
__plugin_implementation__ = i2CLCD2004Plugin()
