import os

def retrive_test_file_directory(file_name):
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, file_name)
