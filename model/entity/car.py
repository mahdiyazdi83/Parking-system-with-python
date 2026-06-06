from tools.validation import Validation

class Car:
    def __init__(self, plate, model, mobile):
        self.plate = plate
        self.model = model
        self.mobile = mobile

    def __repr__(self):
        return f"{self.__dict__}"

    @property
    def plate(self):
        return self.__plate

    @plate.setter
    def plate(self, plate):
        # self.__plate = Validation.plate_validator(plate)
        self.__plate = plate

    @property
    def mobile(self):
        return self.__mobile

    @mobile.setter
    def mobile(self, mobile):
        self.__mobile = Validation.mobile_validator(mobile)