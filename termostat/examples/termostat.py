from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
import RPi.GPIO as GPIO
import Adafruit_DHT
from time import sleep
import urllib.request

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
DHTPin = 17                             #define the pin of DHT11
buzzerPin = 21                          #define the pin of Buzzer
limit = 30                              #define the temperature limit

GPIO.setup(buzzerPin, GPIO.OUT)
GPIO.output(buzzerPin, False)

def loop():
    counts = 0                          # Measurement counts
    mcp.output(3,1)                     # turn on LCD backlight
    lcd.begin(16,2)                     # set number of LCD lines and columns
    destroy()
    lcd.message('Lettura sensori,\navvio in corso..')
    while(True):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTPin)
        if counts < 1 and humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
            alertor(("RaspiServer:\nTermostato attivo! Temperatura iniziale rilevata: {0:0.1f}C").format(temperature))
        elif counts > 0 and humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
        counts=counts+1
        if temperature > 0:
            lcd.setCursor(0,0)          # set cursor position
            message1 = ("Tempera.: {:.1f}").format(temperature)+chr(223)+"  \n"
            message2 = ("Umidita': {:.0%}    ").format(humidity/100)
            lcd.message(message1)
            lcd.message(message2)
            if temperature > limit:
                alertor("RaspiServer:\nRilevata sovra temperature! Temperatura attuale: "+("{:.1f}").format(temperature))
            else:
                sleep(2)
        
def destroy():
    lcd.clear()
    
def alertor(message):
    buzzState = False
    url = "https://toidigitalagency.it/ajax/alert/8/" + urllib.parse.quote_plus(message)
    try:
        webUrl = urllib.request.urlopen(url)
    except:
        print("Errore di connessione! " + url)
        for x in range(0,4):
            buzzState = not buzzState
            GPIO.output(buzzerPin, buzzState)
            sleep(0.5)
    else:
        print(str(webUrl.getcode()))
        for x in range(0,10):
            buzzState = not buzzState
            GPIO.output(buzzerPin, buzzState)
            sleep(0.2)
    
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
        
