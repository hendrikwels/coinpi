from flask import Flask
from flask import render_template, Response
import pulsecount 
import urllib2
from camera import Camera


app = Flask(__name__)

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/getbitcoin/")
def getbitcoin():
	
	balance = pulsecount.Balance
	message = "Moin"
	
	return render_template("getbitcoin.html", balance = balance, message = message)

@app.route("/exchange/")
def exchange():
	balance = pulsecount.Balance
	rate = urllib2.urlopen("https://blockchain.info/de/tobtc?currency=EUR&value={}".format(balance)).read()
	
	return render_template("exchange.html", rate = rate)
	
@app.route("/scanner/")
def scanner():
	
	return render_template("scanner.html")
	
def gen(camera):
	"""Video streaming generator function."""
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
               
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
	
if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", threaded=True)
