from quat import *


if __name__ == "__main__":
    q1 =  [-0.531547, -0.553977, -0.45026, 0.455888]
    q2 =  [-0.711383, -0.701682, 0.035376, -0.018067] #qref

    print euler_from_quaternion(quaternion_multiply(q1,quaternion_conjugate(q2)))
