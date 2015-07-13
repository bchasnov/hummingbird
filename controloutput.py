# controloutput.py

# ControlOutput is a class which includes get and set functions,
# and is mapped to a servo on a ServoBoard


class ControlOutput:
    def __init__(self, servoboard, servo_i):
        self.servoboard = servoboard  # reference to servoboard
        self.index = servo_i

    def get(self):
        return self.servoboard.servo_vals[self.index]

    def set(self, value):
        print "Setting servo", self.index, "to", value
        self.servoboard.servo_vals[self.index] = value
