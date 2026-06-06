class ParkSpot:
    def __init__(self, place, floor):
        self.place = place
        self.floor = floor

    def __repr__(self):
        return f"{self.__dict__}"

    @property
    def place(self):
        return self.__place

    @place.setter
    def place(self, place):
        if not 1 <= place <= 50:
            raise ValueError("place should be between 1 and 50")
        self.__place = place

    @property
    def floor(self):
        return self.__floor

    @floor.setter
    def floor(self, floor):
        if not 1 <= floor <= 8:
            raise ValueError("flor should be between 1 and 8")
        self.__floor = floor