import os
import json
import collections


DIR_NAME = "wifi_data"
REQUIRED_QUANTITY_STREETS = 5

wifi_points_location = []
wifi_streets = []


wifi_input_data = list(
    filter(
        lambda x: x.endswith('.json'),
        os.listdir(DIR_NAME)
       )
    )


def get_initial_wifi_data(filename):
    with open(filename, 'r', encoding="CP1251") as my_file:
        initial_wifi = json.load(my_file)
    return initial_wifi


def get_location_wifi_points(initial_wifi):
    for point in initial_wifi:
        try:
            wifi_point_adress = point['Address']
            wifi_points_location.append(wifi_point_adress)
        except KeyError:
            wifi_point_park_location = point.get('ParkName')
            wifi_points_location.append(wifi_point_park_location)
    return wifi_points_location


def get_street_wifi_points(wifi_points_location, wifi_streets):
    for wifi_point_address in wifi_points_location:
        street = wifi_point_address.partition("дом")
        wifi_streets.append(street[0].rstrip(', '))
    return wifi_streets


def get_count_wifi(wifi_streets):
    count_points = collections.Counter(wifi_streets)
    most_points = count_points.most_common(REQUIRED_QUANTITY_STREETS)
    return most_points


def print_result(most_points):
    print('Больше всего халявных точек wifi: \n')
    for street in most_points:
        print(street[0], street[1], 'шт.')


if __name__ == '__main__':
    for filename in wifi_input_data:
        file_path = os.path.join(DIR_NAME, filename)
        initial_wifi = get_initial_wifi_data(file_path)
        wifi_points_location = get_location_wifi_points(initial_wifi)
    streets = get_street_wifi_points(wifi_points_location, wifi_streets)
    count_points_on_street = get_count_wifi(streets)
    print_result(count_points_on_street)
