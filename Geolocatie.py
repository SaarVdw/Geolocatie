import requests
import pandas as pd
import plotly.express as px

while True:
#benoemen van kaart en kolommen
    print("Geef een titel aan je kaart: ")
    titel = input()
    print("De titel van je kaart is " + titel + ". ")
    print("Heeft je csv-bestand de kolommen: gemeente, straat en huisnummer?")
    juiste_kolommen = input()
    if juiste_kolommen == "ja":
    #controleren of er extra kolommen zijn
        print("Zijn er nog extra kolommen in je csv?")
        extra_kolommen = input()
        if extra_kolommen == "ja" or "neen" or "nee":
            break
        else:
            print("Gelieve te antwoorden met ja of nee")
    else:
        print("Voeg een correct csv-bestand toe met de kolommen: gemeente, straat en huisnummer.")

#controleren of de voorwaarden voor een standaard of gepersonaliseerde kaart aanwezig zijn.
standaard_kaart = extra_kolommen
standaard_kaart == False

gepersonaliseerde_kaart = extra_kolommen
gepersonaliseerde_kaart == False

if standaard_kaart != "ja":
    standaard_kaart == True
    print(titel + " wordt nu gemaakt en zal automatisch in je browser geopend worden. Een nieuw csv bestand met coördinaten wordt in de map geplaatst.")

    # importeer csv met bestandsnaam "adressen.csv", met daarin een lijst met adressen met volgende kolomnamen: [gemeente][straat][huisnummer]
    df = pd.read_csv("adressen.csv")

    # voeg nieuwe kolommen toe om geformatteerde adressenlijst te krijgen
    df.insert(loc=0, column="format", value="https://loc.geopunt.be/v1/Location?q=")
    df.insert(loc=2, column="format2", value="%2C%20")
    df.insert(loc=4, column="format3", value="%20")

    # maak nieuw dataframe met geformatteerde adressen
    df_geformatteerd = df["format"].astype(str) + df["gemeente"].astype(str) + df["format2"].astype(str) + df[
        "straat"].astype(str) + df["format3"].astype(str) + df["huisnummer"].astype(str)

    lijst = df_geformatteerd.tolist()
    lijst_coordinaten = []

    # bevraag endpoint en sla responses op in lijst + omzetting naar dataframe
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
    df_kaart.to_csv("coordinaten.csv", index=False)

    #kaart maken
    fig = px.scatter_mapbox(df_kaart,
                            lat="latitude",
                            lon="longitude",
                            hover_name="adres",
                            title= titel,
                            zoom=11,
                            height=800
                            )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()

if gepersonaliseerde_kaart == "ja":
    gepersonaliseerde_kaart == True
    print(titel + " wordt nu gemaakt en zal automatisch in je browser geopend worden.")

    # importeer csv met bestandsnaam "adressen.csv", met daarin een lijst met adressen met volgende kolomnamen: [gemeente][straat][huisnummer]
    df = pd.read_csv("adressen.csv")

    # voeg nieuwe kolommen toe om geformatteerde adressenlijst te krijgen
    df.insert(loc=0, column="format", value="https://loc.geopunt.be/v1/Location?q=")
    df.insert(loc=2, column="format2", value="%2C%20")
    df.insert(loc=4, column="format3", value="%20")

    # maak nieuw dataframe met geformatteerde adressen
    df_geformatteerd = df["format"].astype(str) + df["gemeente"].astype(str) + df["format2"].astype(str) + df[
        "straat"].astype(str) + df["format3"].astype(str) + df["huisnummer"].astype(str)

    lijst = df_geformatteerd.tolist()
    lijst_coordinaten = []

    # bevraag endpoint en sla responses op in lijst + omzetting naar dataframe
    for value in lijst:
        response = requests.get(value)
        coordinaten = response.json()
        lijst_coordinaten.append(coordinaten)
        df_coordinaten = pd.json_normalize(lijst_coordinaten, "LocationResult")
        df_response = pd.DataFrame(df_coordinaten)

    #extraheren van relevante informatie, omzetten naar nieuw dataframe en kolommen hernoemen
    df_lijst = (df_response.filter(["FormattedAddress","Location.Lat_WGS84","Location.Lon_WGS84"], axis=1))
    df_lijst.rename(columns={"FormattedAddress":"adres", "Location.Lat_WGS84":"latitude","Location.Lon_WGS84":"longitude"}, inplace=True)

    df_info = df
    df_info.insert(loc=0, column="adres", value=(df["straat"] + " " + df["huisnummer"].astype(str) + ", " + df["gemeente"]))
    df_info = df.drop(["straat", "huisnummer", "gemeente", "format", "format2", "format3"], axis=1)
    print(df_info)

    df_kaart = df_lijst.merge(df_info)
    print(df_kaart)
    df_kaart.to_csv("coordinaten.csv", index=False)

    #kaart maken
    fig = px.scatter_mapbox(df_kaart,
                            lat="latitude",
                            lon="longitude",
                            hover_name="adres",
                            title= titel,
                            zoom=11,
                            height=800
                            )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()

aantal_gevonden_coordinaten = len(df_lijst)
print(f"{aantal_gevonden_coordinaten} adressen konden gekoppeld worden aan coördinaten.")





