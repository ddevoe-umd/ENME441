# main.py runs after boot.py

from machine import SoftI2C as I2C
from machine import Pin
from ssd1306 import SSD1306_I2C  # OLED display
import wifi                      # wifi setup

# Set up I2C (neded for the OLED display):
sda = Pin(5)   # may need to swap SDA & SCL pin #s
scl = Pin(4)   # depening on the specfic ESP32 board
i2c = I2C(sda=sda, scl=scl) 

# Scan for I2C devices:
devices = i2c.scan()
print(f'\nI2C devices: ', end='')
for device in devices:  
    print(f'0x{device:02x}', end='  ')
print('\n')

# Set up display:
w = const(128) # screen width
h = const(64)  # screen height
ch = const(8)  # character width/height
display = SSD1306_I2C(w, h, i2c)
display.text('connecting', w//2-5*ch, (h//2)-ch)  #FrameBuffer.text(s, x, y)
display.text('to WiFi', w//2-3*ch, h//2+ch)
display.show()

# Set up WiFi:
ssid = 'ROUTER_SSID'           # Replace with router ssid
password = 'ROUTER_PASSWORD'   # Replace with router password
ip = wifi.connect(ssid, password)
display.fill_rect(0,0,w,h,0)   # clear the screen
display.text(ip, w//2-len(ip)*ch//2, h//2)  # Display the IP (centered)
display.show()

# Run additional code as desired by importing modules
# without __main__ function
#
#import module_name
