import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN)

global revcount
global coinValue
global balance

revcount = 0
coinValue = float(0.00)
balance = float(0.00)

def increaserev(self):
    global revcount
    global coinValue
    global balance
    
    revcount += 1
    
    if revcount == 2:
        coinValue = float(1.00)
        balance += coinValue
    else:
        coinValue = float(0.5)

		balance += coinValue

    


GPIO.add_event_detect(27, GPIO.RISING, callback=increaserev)

while True:
    sleep(2)
    print "Coin Value is {0}".format(coinValue)
    print "Balance is {0}".format(balance)
    revcount = 0
    coinValue = 0
