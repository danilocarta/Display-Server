#!/usr/bin/env python3
#############################################################################
# Filename    : DHT11.py
# Description :	read the temperature and humidity data of DHT11
# Author      : freenove
# modification: 2020/10/16
########################################################################
import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT
DHTPin = 11     #define the pin of DHT11

def loop():
  dht = DHT.DHT(DHTPin)   #create a DHT class object
  for i in range(0,15):            
    chk = dht.readDHT11()     #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
    if (chk is dht.DHTLIB_OK):      #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
       break
    print("Humidity : %.2f, \t Temperature : %.2f \n"%(dht.humidity,dht.temperature))    

try:
  loop()
except KeyboardInterrupt:
  PIO.cleanup()
  exit()  