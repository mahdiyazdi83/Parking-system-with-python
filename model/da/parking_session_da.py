import pickle

def save_to_parking_session_file(data_list):
    my_file = open("parking_session.dat", "wb")
    pickle.dump(data_list, my_file)
    my_file.close()


def read_from_parking_session_file():
    try:
        my_file = open("parking_session.dat", "rb")
        data = pickle.load(my_file)
        my_file.close()
        return data
    except FileNotFoundError:
        save_to_parking_session_file([])
        return []
