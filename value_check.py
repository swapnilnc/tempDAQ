import json


def reload_file_data(file_path):
    data_list = []
    with open(file_path, 'r') as file_reader:
        data_line = file_reader.read().strip()
        if ',' in data_line:
            data_list = list(map(float, data_line.split(',')))
    return data_list


def load_configuration_file(file_path):
    with open(file_path) as json_reader:
        data = json.load(json_reader)
    return data
