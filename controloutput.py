# controloutput.py

# ControlOutput is a class which includes get and set functions,
# and is mapped to a servo on a ServoBoard


class ControlOutput:
    def __init__(self, servoboard, servo_i):
        self.servoboard = servoboard
        self.index = servo_i

    def __get__(self, instance, owner):
        return self.servoboard.servo_vals[self.index]

    def __set__(self, instance, value):
        self.servoboard.servo_vals[self.index] = value
