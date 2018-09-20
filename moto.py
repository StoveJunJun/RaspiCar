from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pan=17
titl=4

GPIO.setup(pan,GPIO.OUT)
GPIO.setup(titl,GPIO.OUT)


def setServoAngle(servo,angle):
    assert angle >=0  and angle<=150
    pwm=GPIO.PWM(servo,50)
    pwm.start(8)
    dutyCycle=angle/18.+3.
    pwm.ChangeDutyCycle(dutyCycle)
    sleep(0.3)
    pwm.stop()
    
    