from datetime import datetime

class ParkingSession:
    def __init__(self, car, spot, out_time=None):
        self.car = car
        self.spot = spot
        self.in_time = datetime.now()
        self.out_time = out_time


    def __repr__(self):
        return f"{self.__dict__}"