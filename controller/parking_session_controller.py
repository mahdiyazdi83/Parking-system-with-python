from model.bl.system_bl import ParkingSessionLogic
from model.entity.parking_session import ParkingSession
from tools.logger_system import Logger


class ParkingSessionController:
    def __init__(self):
        self.bl = ParkingSessionLogic()

    def park_car(self, car, spot):
        try:
            session = ParkingSession(car=car,spot=spot)
            self.bl.park_car(session)
            Logger.info(f"Car {car.plate} parked successfully")
            return "CAR PARKED SUCCESSFULLY"

        except Exception as e:
            Logger.error(f"CAR NOT PARKED : {e}")
            return f"Error : {e}"

    def exit_car(self, plate):
        try:
            cost = self.bl.exit_car(plate)
            Logger.info(f"Car {plate} exited parking")
            return f"COST : {cost}$"

        except Exception as e:
            Logger.error(f"EXIT FAILED : {e}")
            return f"Error : {e}"