import pickle

def write_to_pkl(pkl_file_path, data):
    with open(pkl_file_path, 'wb') as f:
        pickle.dump(data, f)

def load_pkl(pkl_file_path):
    with open(pkl_file_path, 'rb') as f:
        data_loaded = pickle.load(f)
    return data_loaded