# wifi.py
#
# Establish WiFi connection

import network

def connect(ssid, password):   
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    ip = wlan.ifconfig()[0]
    
    return ip

