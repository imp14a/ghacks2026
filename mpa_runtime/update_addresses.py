
import json

def update_addresses():
    san_pablo_addresses = [
        "5 de Febrero No. 26 y 28, Colonia Centro, C.P. 06060, Alcaldía Cuauhtémoc, Ciudad de México.",
        "Isabel la Católica No. 92, Colonia Centro, C.P. 06080, Alcaldía Cuauhtémoc, Ciudad de México.",
        "Eje 2 Canal de Norte No. 107, Colonia Morelos, C.P 06200, Alcaldía Cuauhtémoc, Ciudad de México.",
        "Av. Cuauhtémoc No. 114 y 116 A, Colonia Doctores, C.P. 06720, Alcaldía Cuauhtémoc, Ciudad de México."
    ]
    ahorro_addresses = [
        "Donceles 85",
        "Las Cruces 18",
        "Eje Central Lazaro Cardenas 13 Local G",
        "Belisario Dominguez 3"
    ]
    benavides_addresses = [
        "Av. Universidad No. 1293, Col. del Valle, Benito Juárez, Cdmx, CP. 03240.",
        "Av. Presidente Masaryk #490, Colonia Polanco, Delegación Miguel Hidalgo, CP. 11560, Mexico, Distrito Federal.",
        "Av. Insurgentes 197, Roma Norte, Cuauhtémoc, Ciudad de México, CP 06700.",
        "Av. Capitán Carlos León, s/n, México D.F."
    ]
    similares_addresses = [
        "Tacuba, 69, Ciudad de México",
        "Cll. Regina 51, Cuauhtémoc (CDMX)",
        "Emiliano Zapata, 59, Ciudad de México",
        "Vasco de Quiroga 3900, Lomas de Santa Fe, Contadero, Cuajimalpa de Morelos, 01219 Ciudad de México, CDMX, México"
    ]
    yza_addresses = [
        "Calle 47 75",
        "Calle Jesus Romero Flores #No. 92, Iztapalapa",
        "Calle Leibnitz 8, Anzures",
        "Av. Luis Manuel Rojas 9, Constitución de 1917, Iztapalapa, 09260 Ciudad de México, CDMX"
    ]

    with open("/usr/local/google/home/agusramirez/cloud/genai/gchacks2026/mpa_runtime/mpa/sub_agents/inventory_agent/mock_inventory.json", "r") as f:
        pharmacies = json.load(f)

    san_pablo_index = 0
    ahorro_index = 0
    benavides_index = 0
    similares_index = 0
    yza_index = 0

    for pharmacy in pharmacies:
        if pharmacy["name"] == "Farmacia San Pablo":
            pharmacy["address"] = san_pablo_addresses[san_pablo_index % len(san_pablo_addresses)]
            san_pablo_index += 1
        elif pharmacy["name"] == "Farmacias del Ahorro":
            pharmacy["address"] = ahorro_addresses[ahorro_index % len(ahorro_addresses)]
            ahorro_index += 1
        elif pharmacy["name"] == "Farmacias Benavides":
            pharmacy["address"] = benavides_addresses[benavides_index % len(benavides_addresses)]
            benavides_index += 1
        elif pharmacy["name"] == "Farmacias Similares":
            pharmacy["address"] = similares_addresses[similares_index % len(similares_addresses)]
            similares_index += 1
        elif pharmacy["name"] == "Farmacias YZA":
            pharmacy["address"] = yza_addresses[yza_index % len(yza_addresses)]
            yza_index += 1

    with open("/usr/local/google/home/agusramirez/cloud/genai/gchacks2026/mpa_runtime/mpa/sub_agents/inventory_agent/mock_inventory.json", "w") as f:
        json.dump(pharmacies, f, indent=4)

if __name__ == "__main__":
    update_addresses()
