import os
import json
import collections
import requests
import settings
import logging


DIR_NAME = "wifi_data"
REQUIRED_QUANTITY_POINTS = 5
logging.basicConfig(filename='wifi.log', filemode='w')

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


def fetch_wifi_coordinates(initial_wifi):
    for point in initial_wifi:
        wifi_point_coordinates = {
            'latitude': point['Latitude_WGS84'],
            'longitude': point['Longitude_WGS84'],
        }
        wifi_points_location.append(wifi_point_coordinates)
    return wifi_points_location


def fetch_streets_data(api_key, coordinates):
    base_url = 'https://geocode-maps.yandex.ru/1.x'
    params = {
        'apikey': api_key,
        'format': 'json',
        'geocode': coordinates,
        'kind': 'street',
        'results': '1'
        }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    street_data = response.json()
    return street_data


def get_street_wifi_points(street_data):
    try:
        name_street = street_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['Components'][4]['name']
        wifi_streets.append(name_street)
    except IndexError:
        logging.exception('пустой список')
    return wifi_streets


def get_count_wifi(wifi_streets):
    count_points = collections.Counter(wifi_streets)
    most_points = count_points.most_common(REQUIRED_QUANTITY_POINTS)
    return most_points


def print_result(most_points):
    print('Больше всего халявных точек wifi: \n')
    for street in most_points:
        print(street[0], street[1], 'шт.')


if __name__ == '__main__':
    for filename in wifi_input_data:
        file_path = os.path.join(DIR_NAME, filename)
        initial_wifi = get_initial_wifi_data(file_path)
        wifi_points_location = fetch_wifi_coordinates(initial_wifi)
    for point in wifi_points_location:
        coordinate = point['longitude'], point['latitude']
        geocode = ','.join(coordinate)
        street_data = fetch_streets_data(settings.API_KEY, geocode)
        streets = get_street_wifi_points(street_data)
    count_points_on_street = get_count_wifi(streets)
    print_result(count_points_on_street)
