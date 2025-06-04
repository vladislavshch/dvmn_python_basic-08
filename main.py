import json
import requests
import folium
from geopy import distance
from decouple import config


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_min_distance(cafe):
    return cafe['Distance']


def main():
    apikey = config('yandex_apikey')
    with open ('coffee.json', 'r', encoding='CP1251') as coffee_file:
        file_contents = coffee_file.read()
    coffee_houses = json.loads(file_contents)

    coffee_shop = dict()
    coffee_shops = []

    where_are_you = input('Где Вы находитесь: ')
    coords = fetch_coordinates(apikey, where_are_you)
    coords_list = list(coords)
    coords_list[0], coords_list[-1] = coords_list[-1], coords_list[0]
    coords = coords_list

    for coffee in coffee_houses:
        coffee_shop['Title'] = coffee['Name']
        coffee_location = coffee['geoData']['coordinates']
        coffee_coordinates = list(coffee_location)
        coffee_coordinates[0], coffee_coordinates[-1] = coffee_coordinates[-1], coffee_coordinates[0]
        coffee_shop['Distance'] = distance.distance(coords, coffee_coordinates).km
        coffee_shop['Latitude'] = coffee['Latitude_WGS84']
        coffee_shop['Longitude'] = coffee['Longitude_WGS84']
        coffee_shops.append(coffee_shop)
        coffee_shop = dict()

    sorted_coffee = sorted(coffee_shops, key=get_min_distance)
    coffee_list = []

    for coffees in sorted_coffee:
        coffee_name = coffees
        coffee_list.append(coffee_name)

    number_of_coffees = 5
    nearby_coffee_shops = []
    for coffees_number in range(0, len(coffee_list), number_of_coffees):
        nearby_coffee_shop = coffee_list[coffees_number:coffees_number + number_of_coffees]
        nearby_coffee_shops.append(nearby_coffee_shop)

    m = folium.Map(location=coords)
    group_coffee = folium.FeatureGroup('coffee group').add_to(m)
    folium.Marker(
        (float(nearby_coffee_shops[0][0]['Latitude']), float(nearby_coffee_shops[0][0]['Longitude'])),
        popup=nearby_coffee_shops[0][0]['Title'],
        icon=folium.Icon("red"),
    ).add_to(group_coffee)
    folium.Marker(
        (float(nearby_coffee_shops[0][1]['Latitude']), float(nearby_coffee_shops[0][1]['Longitude'])),
        popup=nearby_coffee_shops[0][1]['Title'],
        icon=folium.Icon("red"),
    ).add_to(group_coffee)
    folium.Marker(
        (float(nearby_coffee_shops[0][2]['Latitude']), float(nearby_coffee_shops[0][2]['Longitude'])),
        popup=nearby_coffee_shops[0][2]['Title'],
        icon=folium.Icon("red"),
    ).add_to(group_coffee)
    folium.Marker(
        (float(nearby_coffee_shops[0][3]['Latitude']), float(nearby_coffee_shops[0][3]['Longitude'])),
        popup=nearby_coffee_shops[0][3]['Title'],
        icon=folium.Icon("red"),
    ).add_to(group_coffee)
    folium.Marker(
        (float(nearby_coffee_shops[0][4]['Latitude']), float(nearby_coffee_shops[0][4]['Longitude'])),
        popup=nearby_coffee_shops[0][4]['Title'],
        icon=folium.Icon("red"),
    ).add_to(group_coffee)
    folium.LayerControl().add_to(m)
    m.save("index.html")


if __name__ == '__main__':
    main()



