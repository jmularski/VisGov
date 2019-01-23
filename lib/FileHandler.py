import pickle

class FileHandler():
    def __init__(self):
        pass

    def save_file(self, name, object):
        with open('../output/'+ name + '.pkl', 'wb') as f:
            pickle.dump(object, f, pickle.HIGHEST_PROTOCOL)
    
    def load_file(self, name):
        with open('output/' + name + '.pkl', 'rb') as f:
            return pickle.load(f)