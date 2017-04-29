
class PID:

    def __init__(self, kp=0.0, ki=0.0, kd=0.0, dt=0.1):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.e0 = 0.0
        self.e1 = 0.0
        self.e2 = 0.0
        self.dt = dt
        self.u = 0.0

    def step(self, e, dt=None):
        self.e2 = self.e1
        self.e1 = self.e0
        self.e0 = e

        if dt is None:
            delta_t = self.dt
        else:
            delta_t = dt

        self.u += self.e0 * (self.kp + self.ki * delta_t + self.kd / delta_t) + \
                  self.e1 * (-self.kp -2 * self.kd / delta_t ) + \
                  self.e2 * (self.kd / delta_t)

        return self.u


