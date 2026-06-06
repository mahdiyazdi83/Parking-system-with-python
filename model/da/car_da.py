import pickle

def save_to_car_file(data_list):
    my_file = open("car.dat", "wb")
    pickle.dump(data_list, my_file)
    my_file.close()


def read_from_car_file():
    try:
        my_file = open("car.dat", "rb")
        data = pickle.load(my_file)
        my_file.close()
        return data
    except FileNotFoundError:
        save_to_car_file([])
        return []
