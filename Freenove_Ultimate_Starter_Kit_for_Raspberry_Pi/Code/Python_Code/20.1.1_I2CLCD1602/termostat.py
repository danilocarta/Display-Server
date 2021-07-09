#!/usr/bin/env python3
########################################################################
# Filename    : I2CLCD1602.py
# Description : Use the LCD display data
# Author      : freenove
# modification: 2018/08/03
########################################################################
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
import RPi.GPIO as GPIO
import Freenove_DHT as DHT
from time import sleep
DHTPin = 11     #define the pin of DHT11
  
def loop():
    destroy()
    dht = DHT.DHT(DHTPin)   #create a DHT class object
    counts = 0
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
    lcd.setCursor(0,0)  # set cursor position
    lcd.message("Lettura Sensori\navvio in corso..")
    while(True):  
        counts += 1
        for i in range(0,15):            
            chk = dht.readDHT11()     #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
            if (chk is dht.DHTLIB_OK):      #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
                break
            sleep(0.1)        
        if counts == 1:
            destroy()
        lcd.setCursor(0,0)  # set cursor position
        message1 = "Tempera.: {:.1f}".format(dht.temperature)+chr(223)
        message2 = "Umidita': {:.0%}".format(dht.humidity/100)
        lcd.message(message1+'\n')  # display external temperature
        lcd.message(message2)       # display external humidity
        sleep(2)
        
        
def destroy():
    lcd.clear()
    
PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

if __name__ == '__main__':
    print ('Avvio programma... ')
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
        destroy()
        exit()
