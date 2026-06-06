import pickle

def save_to_park_spot_file(data_list):
    my_file = open("park_spot.dat", "wb")
    pickle.dump(data_list, my_file)
    my_file.close()


def read_from_park_spot_file():
    try:
        my_file = open("park_spot.dat", "rb")
        data = pickle.load(my_file)
        my_file.close()
        return data
    except FileNotFoundError:
        save_to_park_spot_file([])
        return []
