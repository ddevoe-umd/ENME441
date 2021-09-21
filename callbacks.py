import RPi.GPIO as gpio

# Define input port numbers:
in1, in2 = 17, 27

gpio.setmode(gpio.BCM)
gpio.setup(in1, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(in2, gpio.IN, pull_up_down=gpio.PUD_DOWN)

# Define a threaded callback function:
def myCallback(channel):
  print("Rising edge detected on pin %d" % channel)

# Execute myCallback() if port 1 goes HIGH:
gpio.add_event_detect(in1, gpio.RISING, callback=myCallback, bouncetime=100)

# pause main code until port 2 goes LOW:
gpio.wait_for_edge(in2, gpio.FALLING)
print("Falling edge detected on port", str(in2))

gpio.cleanup()
