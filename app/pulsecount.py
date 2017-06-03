import RPi.GPIO as GPIO
from time import sleep
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN)

global revcount
global coinValue
global Balance

revcount = 0
coinValue = float(0.00)
Balance = float(0.00)

def increaserev(self):
    global revcount
    global coinValue
    global Balance
    
    revcount += 1
    
    if revcount == 2:
        coinValue = float(1.00)
        
    else:
        coinValue = float(0.5)


GPIO.add_event_detect(27, GPIO.RISING, callback=increaserev)
def do_work():
	global revcount
	global coinValue
	global Balance
	while True:
		sleep(2)
		if revcount > 0:
			Balance += coinValue
			print "Coin Value is {0}".format(coinValue)
			print "Balance is {0}".format(Balance)
	
			revcount = 0
			#coinValue = 0
		sleep(0.2)
		
worker = threading.Thread(target=do_work,name='myworker')
worker.daemon = True
worker.start()

