# Display-Server for Raspberry Zero or higghest
To show temp on server room and call a url on over temp limit.<br/>
You Need:
<ul>
<li>1 Raspberry Zero or Higher</li>
<li>1 DHT11 or DHT22 to measure temp and humidity</li>
<li>1 I2C Display 16 digit for 2 rows, LCD1602</li>
<li>1 Buzzer</li>
<li>1 Resistor with 10kOhm</li>
</ul>

# Essentials if you haven't
```
sudo raspi-config
```
> 9 Advanced Options<br/>
> A7 I2C and Enable it
```
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install i2c-tools
sudo apt-get install python3-smbus
sudo python3 -m pip install --upgrade pip setuptools wheel
```

# Install process
```
cd termostat/
python3 setup.py
python3 examples/termostat.py
```

# Data sheet schema
<img src="/fritzing_data_sheet.png">

