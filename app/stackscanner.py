import cv2
import cv2.cv as cv
import numpy
import zbar
import time
import threading
#from camera import Camera

'''
LITTLE-DELAY BarCodeScanner
Author: Chen Jingyi (From FZYZ Junior High School, China)
PS. If your pi's V4L is not available, the cv-Window may have some error sometimes, but other parts of this code works fine.
'''
class BarCodeScanner(threading.Thread):
    def __init__(self):
		threading.Thread.__init__(self)

		self.WINDOW_NAME = 'Camera'
		self.CV_SYSTEM_CACHE_CNT = 5 # Cv has 5-frame cache
		self.LOOP_INTERVAL_TIME = 0.2

		cv.NamedWindow(self.WINDOW_NAME, cv.CV_WINDOW_NORMAL)
		self.cam = cv2.VideoCapture(-1)

    def scan(self, aframe):
		imgray = cv2.cvtColor(aframe, cv2.COLOR_BGR2GRAY)
		raw = str(imgray.data)

		scanner = zbar.ImageScanner()
		scanner.parse_config('enable')          

		#print 'ScanZbar', time.time()
		width = int(self.cam.get(cv.CV_CAP_PROP_FRAME_WIDTH))
		height = int(self.cam.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
		imageZbar = zbar.Image(width, height,'Y800', raw)
		scanner.scan(imageZbar)
		#print 'ScanEnd', time.time()

		for symbol in imageZbar:
			print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data

    def run(self):
        #print 'BarCodeScanner run', time.time()
        while True:
            #print time.time()
            ''' Why reading several times and throw the data away: I guess OpenCV has a `cache-queue` whose length is 5.
            `read()` will *dequeue* a frame from it if it is not null, otherwise wait until have one.
            When the camera has a new frame, if the queue is not full, the frame will be *enqueue*, otherwise be thrown away.
            So in this case, the frame rate is far bigger than the times the while loop is executed. So when the code comes to here, the queue is full.
            Therefore, if we want the newest frame, we need to dequeue the 5 frames in the queue, which is useless because it is old. That's why.
            '''
            for i in range(0,self.CV_SYSTEM_CACHE_CNT):
                #print 'Read2Throw', time.time()
                self.cam.read()
            #print 'Read2Use', time.time()
            img = self.cam.read()
            self.scan(img[1])

            cv2.imshow(self.WINDOW_NAME, img[1])
            cv.WaitKey(1)
            #print 'Sleep', time.time()
            time.sleep(self.LOOP_INTERVAL_TIME)

        cam.release()

scanner = BarCodeScanner()
scanner.start()
