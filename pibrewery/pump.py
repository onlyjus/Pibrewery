from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor


class Pump(object):

    def __init__(self, motor=4, direction=0):

        self.speed = 150
        self.direction = Adafruit_MotorHAT.FORWARD
        if direction == 1:
            self.direction = Adafruit_MotorHAT.BACKWARD

        self.mh = Adafruit_MotorHAT(addr=0x60)
        self.pump = self.mh.getMotor(motor)
        
        # turn on motor
        self.pump.run(Adafruit_MotorHAT.RELEASE);
        self.pump.run(self.direction)

    def set_speed(self, speed=150):
        self.speed = speed
        self.pump.setSpeed(int(speed))


    def off(self):
        self.pump.run(Adafruit_MotorHAT.RELEASE)


if __name__ == "__main__":

    import time

    pump = Pump(4, 1)
    pump.set_speed(200)
    time.sleep(10)
    pump.off()
