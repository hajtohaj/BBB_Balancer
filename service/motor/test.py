from motor import Motor
import time

if __name__ == "__main__":

    m0 = Motor(0)
    m1 = Motor(1)

    while 1:
        print(m0.get_position(), m1.get_position())
        time.sleep(0.25)