import time
import io
import threading
import picamera
import cv2
import cv2.cv as cv
import numpy
import zbar
#import stackscanner
	


class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera
    

    def initialize(self):
		
			
		if Camera.thread is None:
			# start background frame thread
			Camera.thread = threading.Thread(target=self._thread)
			Camera.thread.start()
			self.CV_SYSTEM_CACHE_CNT = 5 # Cv has 5-frame cache
			self.LOOP_INTERVAL_TIME = 0.2
			self.cam = cv2.VideoCapture(-1)
			
		# wait until frames start to be available
		while self.frame is None:
			time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame
        
        imgray = cv2.cvtColor(self, cv2.COLOR_BGR2GRAY)
        raw = str(imgray.data)
        scanner = zbar.ImageScanner()
        scanner.parse_config('enable')     
        
        imageZbar = zbar.Image(width, height,'Y800', raw)
        scanner.scan(imageZbar)
        
        for symbol in imageZbar:
            print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data


	def run(self):
		while True:
			for i in range(0,self.CV_SYSTEM_CACHE_CNT):
				self.cam.read()
				
			img = self.cam.read()
			self.scan(img[1])
			cv2.imshow('image', img[1])
			cv.WaitKey(1)
			time.sleep(self.LOOP_INTERVAL_TIME)
		cam.release()   
	
    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (320, 320)
            camera.hflip = True
            camera.vflip = False

            # let camera warm up
            #~ camera.start_preview()
            #~ time.sleep(2)

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # store frame
                stream.seek(0)
                cls.frame = stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
                
                if time.time() - cls.last_access > 10:
					break
				# if there hasn't been any clients asking for frames in
				# the last 10 seconds stop the thread
		#camera.close()
				
					
		cls.thread = None
	
                
       

                
