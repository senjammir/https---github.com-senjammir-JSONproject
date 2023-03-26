import json


infile_univ = open("univ.json","r")
univ_data = json.load(infile_univ)

infile_schools = open("schools.geojson", "r")
schools_data = json.load(infile_schools)


uni_list = []

for uni in univ_data:
    if uni["NCAA"]["NAIA conference number football (IC2020)"] == 108:
        name = uni["instnm"]
        lat = uni["Latitude location of institution (HD2020)"]
        long = uni["Longitude location of institution (HD2020)"]
        total_enrollment = uni["Total  enrollment (DRVEF2020)"]
        female_percent = uni["Percent of total enrollment that are women (DRVEF2020)"]
        female = (total_enrollment * female_percent) / 100
        male = total_enrollment - female
        for i in schools_data["features"]:
            if i["properties"]["NAME"] == name:
                street = street = i["properties"]["STREET"]
                city = i["properties"]["CITY"]
                state = i["properties"]["STATE"]
                zip = i["properties"]["ZIP"]
                address = (f"{street} {city} {state} {zip}")
                uni_list.append({'Name': name,
                                    'Address': address,
                                    'Total Enrollment': total_enrollment,
                                    'Male': round(male),
                                    'Female': round(female),
                                    'lat': lat,
                                    'long': long })

import folium 

lons, lats, enrollments, names, addresses, males, females = [], [], [], [], [], [], []

for cor in uni_list:
    lons.append(cor['long'])
    lats.append(cor['lat'])
    enrollments.append(cor['Total Enrollment'])
    names.append(cor['Name'])
    addresses.append(cor['Address'])
    males.append(cor['Male'])
    females.append(cor['Female'])

from plotly.graph_objs import Scattergeo, Layout
from plotly import offline

marker = {'size':[enrollment/1000 for enrollment in enrollments], 'color': enrollments,
        'colorscale': 'blues', 'colorbar': {'title': 'Total Enrollment'}
        }

m = folium.Map(location=[lat[0], lons[0]], zoom_start=6)

my_data = Scattergeo(lon=lons, lat=lats, marker=marker)
my_layout = Layout(title='Big 12 Schools', hovermode = 'closest')


fig = {'data':my_data, 'layout':my_layout}

offline.plot(fig, filename='big12_schools.html')