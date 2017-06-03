import time
import io
import threading
import picamera
import cv2
import cv2.cv as cv
import numpy
import zbar
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera
    

    def initialize(self):
		self.cam = cv2.VideoCapture(-1) #keine ob das notig ist
		if Camera.thread is None:
			# start background frame thread
			Camera.thread = threading.Thread(target=self._thread)
			Camera.thread.start()
				
		# wait until frames start to be available
		while self.frame is None:
			time.sleep(0)
			
    def get_frame(self, aframe):
        Camera.last_access = time.time()
        self.initialize()
        
        imgray = cv2.cvtColor(aframe, cv2.COLOR_BGR2GRAY)
        raw = str(imgray.data)
        
        
        scanner = zbar.ImageScanner()
        scanner.parse_config('enable')  
        width = int(self.cam.get(cv.CV_CAP_PROP_FRAME_WIDTH))
        height = int(self.cam.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
        imageZbar = zbar.Image(width, height,'Y800', raw)
        scanner.scan(imageZbar)
		
        for symbol in imageZbar:
            print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
        return self.frame	
        
      
	
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
                
            

                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
		#camera.close()
                if time.time() - cls.last_access > 10:
                    break
		
        cls.thread = None
	
