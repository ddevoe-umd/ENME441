from machine import SoftI2C as I2C
from machine import Pin

# Set up I2C (neded for the OLED display):
sda = Pin(5)   # may need to swap SDA & SCL pin #s
scl = Pin(4)   # depening on the specfic ESP32 board
i2c = I2C(sda=sda, scl=scl) 
 
print('Scan I2C bus...')
devices = i2c.scan()
 
if len(devices) == 0:
  print("No I2C device found")
else:
  print(f'I2C device count: {len(devices)}')
  for device in devices:  
    print(f'Device address: {hex(device)}')
