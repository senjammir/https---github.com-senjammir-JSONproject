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

lons, lats, hover_text, enrollments = [], [], [], []

for cor in uni_list:
    lons.append(cor['long'])
    lats.append(cor['lat'])
    enrollment = (cor['Total Enrollment'])
    enrollments.append(enrollment)
    name = cor['Name']
    address = (cor['Address'])
    male = cor['Male']
    female = cor['Female']
    hover_text.append(f"Name: {name}<br>Address: {address}<br>Total Enrollment: {enrollment}<br>Male: {male}<br>Female: {female}")

from plotly.graph_objs import Scattergeo, Layout
from plotly import offline


my_data = [{
    'type': 'scattergeo',
    'lon': lons,
    'lat': lats,
    'text': hover_text,
    'marker': {
        'size': [e/1000 for e in enrollments],
        'color': enrollments,
        'colorscale': 'twilight',
        'colorbar': {'title': 'Total Enrollment'}
    }
}]
my_layout = Layout(title='Big 12 Schools')


fig = {'data':my_data, 'layout':my_layout}

offline.plot(fig, filename='big12_schools.html')