import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

currentAngle = 0
minDelayTime = 1000
seq = [ [1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],
        [0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1] ]
seq.reverse()
currentState = 0

pins = [14,15,18,23] # controller inputs: in1, in2, in3, in4
for pin in pins:
  GPIO.setup(pin, GPIO.OUT, initial=0)

def delay_us(tus): # use microseconds to improve time resolution
  endTime = time.time() + float(tus)/ float(1E6)
  while time.time() < endTime:
    pass

def sgn(val):   # signum function
  return(int(val/abs(val)))

def step(dir):
  global currentState
  currentState += dir
  if currentState > 7:
    currentState = 0
  elif currentState < 0:
    currentState = 7
  for pin in range(4):
    GPIO.output(pins[pin], seq[currentState][pin])

def goAngle(newAngle, speed):
  global currentAngle
  deltaAngle = newAngle - currentAngle
  if abs(deltaAngle) > 180:
    deltaAngle = (abs(deltaAngle)-180)*(-sgn(deltaAngle))
  if speed > 1:
    speed = 1
  elif speed <= 0:
    speed = 0.05
  # 512 cycle/rev * 1/360 rev/degree * 8 step/cycle = 11.378 step/degree
  stepsPerDegree = 11.378
  numSteps = abs(int(stepsPerDegree * deltaAngle))
  direction = sgn(deltaAngle)
  for s in range(numSteps):
    step(direction)
    delay_us(minDelayTime/speed)
  currentAngle = newAngle

try:
  goAngle(90, 0.8)   # (angle, fractional speed)
  time.sleep(1)
except Exception as e:
  print(e)
GPIO.cleanup()
