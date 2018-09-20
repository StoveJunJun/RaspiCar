# -*- coding: utf-8 -*-
from flask import Flask,render_template,Response
import os 
from time import  sleep
app=Flask(__name__)
import BasicMove as BM
import thread
from camera_pi import Camera
from moto import setServoAngle

global speed
speed=30

global panServoAngle
global tiltSetvoAngle

panServoAngle=90
tiltSetvoAngle=-10

pan=17
tilt=4


@app.route('/')
def index():
    """小车移动"""
    templateData={
        'speed':speed
    }
    return render_template('index.html',**templateData)
	
def gen(camera):
    while True:
        frame=camera.get_frame()
        yield  (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n')


@app.route("/<servo>/<angle>")
def anglemove(servo,angle):
    global panServoAngle
    global tiltSetvoAngle
    if servo=='pan':
        if angle=='+':
            if panServoAngle > 150:
                panServoAngle=150
            panServoAngle=panServoAngle+10
        else:
            if panServoAngle <= 0:
                panServoAngle=0
            panServoAngle=panServoAngle-10
        setServoAngle(pan, panServoAngle)
    if servo == 'tilt':
        if angle == '+':
            if tiltSetvoAngle>40:
                tiltSetvoAngle=40
            tiltSetvoAngle = tiltSetvoAngle+10
        else:
            if tiltSetvoAngle <=-10:
                tiltSetvoAngle =-10
            tiltSetvoAngle = tiltSetvoAngle-10
        setServoAngle(tilt, tiltSetvoAngle)
    templateData={
        'panServoAngle': panServoAngle,
        'tiltSetvoAngle': tiltSetvoAngle
    }
    return render_template('index.html',**templateData)

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),mimetype='multipart/x-mixed-replace;boundary=frame')

	
@app.route("/<mode>/")
def move(mode):
    global speed
    global close_times
    if mode == 'up':
        BM.t_up(speed, 0)
    if mode == 'back':
        BM.t_down(speed, 0)
    if mode == 'left':
        BM.t_left(speed, 1)
        BM.t_stop(0)
    if mode == 'right':
        BM.t_right(speed, 1)
        BM.t_stop(0)
    if mode == 'stop':
	    BM.t_stop(0)
    if mode == 'SpeedUp':
        if(speed < 90) == True:
            speed=speed+5
    if mode == 'SpeedDown':
        if(speed > 10) == True:
            speed=speed-5
    templateData = {
            'speed': speed
        }
    return render_template('index.html', **templateData)



if __name__ == '__main__':
    thread.start_new_thread( BM.loop, () )
    try:
        app.run(debug=True, host='0.0.0.0', port=5000,threaded=True)#在局域网内任意主机访问ip地址:5000即可加载出网页
    except KeyboardInterrupt:
        print("quit")
        BM.GPIO.cleanup()
        sys.quit()
