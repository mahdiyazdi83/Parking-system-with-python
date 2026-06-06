from model.da.car_da import *
from model.da.park_spot_da import *
from model.da.parking_session_da import *
from datetime import datetime


class CarBusinessLogic:
    def __init__(self):
        self.car_list = read_from_car_file()

    def save(self, car):
        for item in self.car_list:
            if item.plate == car.plate:
                raise ValueError("this plate already exists")
        self.car_list.append(car)
        save_to_car_file(self.car_list)

    def find_by_plate(self, plate):
        for car in self.car_list:
            if car.plate == plate:
                return car
        return None

    def get_car_list(self):
        return read_from_car_file()


class ParkSpotLogic:
    def __init__(self):
        self.park_slot_list = read_from_park_spot_file()

    def save(self, park_slot):
        if not 0 < park_slot.place <= 50:
            raise ValueError("parking spot place doesnt exist!")
        if not 1 <= park_slot.floor <= 8:
            raise ValueError("parking spot floor doesnt exist!")
        self.park_slot_list.append(park_slot)
        save_to_park_spot_file(self.park_slot_list)

    def get_park_spot_list(self):
        return read_from_park_spot_file()


class ParkingSessionLogic:
    """$"""
    cost_per_hour = 2

    def __init__(self):
        self.session_list = read_from_parking_session_file()

    def park_car(self, session):
        for item in self.session_list:
            if (item.spot.floor == session.spot.floor and item.spot.place == session.spot.place and item.out_time is None):
                raise ValueError(
                    "parking spot occupied"
                )
        self.session_list.append(session)
        save_to_parking_session_file(self.session_list)

    def exit_car(self, plate):
        for session in self.session_list:
            if (session.car.plate == plate and session.out_time is None):
                session.out_time = datetime.now()
                cost = self.calculate_cost(session)
                save_to_parking_session_file(self.session_list)
                return cost
        raise ValueError("car not found")

    def calculate_cost(self, session):
        duration = (session.out_time - session.in_time).total_seconds() / 3600
        return max(1, int(duration)) * self.cost_per_hour
