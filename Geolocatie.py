import requests
import pandas as pd
import plotly.express as px

#importeer csv met bestandsnaam "adressen.csv", met daarin een lijst met adressen met volgende kolomnamen: [gemeente][straat][nummer]
df = pd.read_csv("adressen.csv")

#voeg nieuwe kolommen toe om geformatteerde adressenlijst te krijgen
df.insert(loc=0, column="format", value="https://loc.geopunt.be/v1/Location?q=")
df.insert(loc=2, column="format2", value="%2C%20")
df.insert(loc=4, column="format3", value="%20")

#maak nieuw dataframe met geformatteerde adressen
df_geformatteerd = df["format"].astype(str) + df["gemeente"].astype(str) + df["format2"].astype(str) + df["straat"].astype(str) + df["format3"].astype(str) + df["huisnummer"].astype(str)

lijst = df_geformatteerd.tolist()
lijst_coordinaten = []

#bevraag endpoint en sla responses op in lijst + omzetting naar dataframe
for value in lijst:
    response = requests.get(value)
    coordinaten = response.json()
    lijst_coordinaten.append(coordinaten)
    df_coordinaten = pd.json_normalize(lijst_coordinaten, "LocationResult")
    df_response = pd.DataFrame(df_coordinaten)

#extraheren van relevante informatie, omzetten naar nieuw dataframe en kolommen hernoemen
df_kaart = df_response.filter(["FormattedAddress","Location.Lat_WGS84","Location.Lon_WGS84"], axis = 1)
df_kaart.rename(columns={"FormattedAddress":"adres", "Location.Lat_WGS84":"latitude","Location.Lon_WGS84":"longitude"}, inplace=True)
print(df_kaart)
df_kaart.to_csv("coordinaten.csv")

#kaart maken
fig = px.scatter_mapbox(df_kaart,
                        lat="latitude",
                        lon="longitude",
                        hover_name="adres",
                        title="test",
                        zoom=11,
                        height=800
                        )
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()







