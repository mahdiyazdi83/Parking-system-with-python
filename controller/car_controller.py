from model.bl.system_bl import CarBusinessLogic
from model.entity.car import Car


class CarController:
    def __init__(self):
        self.bl = CarBusinessLogic()

    def find_by_plate(self, plate):
        return self.bl.find_by_plate(plate)

    def save(self, plate, model, mobile):
        try:
            car = Car(plate, model, mobile)
            self.bl.save(car)
            return "CAR SAVED"

        except Exception as e:
            return f"Error : {e}"