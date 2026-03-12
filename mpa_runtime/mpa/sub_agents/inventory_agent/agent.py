import json
import os
import random
from google.adk.agents.llm_agent import Agent

MOCK_DATA = """
[{"name":"Farmacia San Pablo","address":"5 de Febrero No. 26 y 28, Colonia Centro, C.P. 06060, Alcaldía Cuauhtémoc, Ciudad de México.","branch_number":1},{"name":"Farmacias Benavides","address":"Av. Universidad No. 1293, Col. del Valle, Benito Juárez, Cdmx, CP. 03240.","branch_number":3},{"name":"Farmacias Similares","address":"Tacuba, 69, Ciudad de México","branch_number":4},{"name":"Farmacias YZA","address":"Calle 47 75","branch_number":5},{"name":"Farmacia San Pablo","address":"Isabel la Católica No. 92, Colonia Centro, C.P. 06080, Alcaldía Cuauhtémoc, Ciudad de México.","branch_number":6},{"name":"Farmacias del Ahorro","address":"Las Cruces 18","branch_number":7},{"name":"Farmacias Benavides","address":"Av. Presidente Masaryk #490, Colonia Polanco, Delegación Miguel Hidalgo, CP. 11560, Mexico, Distrito Federal.","branch_number":8},{"name":"Farmacias Similares","address":"Cll. Regina 51, Cuauhtémoc (CDMX)","branch_number":9},{"name":"Farmacias YZA","address":"Calle Jesus Romero Flores #No. 92, Iztapalapa","branch_number":10},{"name":"Farmacia San Pablo","address":"Eje 2 Canal de Norte No. 107, Colonia Morelos, C.P 06200, Alcaldía Cuauhtémoc, Ciudad de México.","branch_number":11},{"name":"Farmacias del Ahorro","address":"Eje Central Lazaro Cardenas 13 Local G","branch_number":12},{"name":"Farmacias Benavides","address":"Av. Insurgentes 197, Roma Norte, Cuauhtémoc, Ciudad de México, CP 06700.","branch_number":13},{"name":"Farmacias Similares","address":"Emiliano Zapata, 59, Ciudad de México","branch_number":14},{"name":"Farmacias YZA","address":"Calle Leibnitz 8, Anzures","branch_number":15},{"name":"Farmacia San Pablo","address":"Av. Cuauhtémoc No. 114 y 116 A, Colonia Doctores, C.P. 06720, Alcaldía Cuauhtémoc, Ciudad de México.","branch_number":16},{"name":"Farmacias del Ahorro","address":"Belisario Dominguez 3","branch_number":17},{"name":"Farmacias Benavides","address":"Av. Capitán Carlos León, s/n, México D.F.","branch_number":18},{"name":"Farmacias Similares","address":"Vasco de Quiroga 3900, Lomas de Santa Fe, Contadero, Cuajimalpa de Morelos, 01219 Ciudad de México, CDMX, México","branch_number":19},{"name":"Farmacias YZA","address":"Av. Luis Manuel Rojas 9, Constitución de 1917, Iztapalapa, 09260 Ciudad de México, CDMX","branch_number":20}]
"""


def find_medicine(medicine_name: str):
    """
    Searches for a medicine product.

    Args:
        medicine_name: The name of the medicine to search for (e.g., 'Paracetamol', 'Ibuprofen').

    Returns:
        A list of pharmacy objects containing the found medicine product, its price and inventory.
    """

    inventory_data = json.loads(MOCK_DATA)

    results = []

    # Pick randomly from 1 to 3 pharmacies
    print(inventory_data)
    num_pharmacies = random.randint(1, min(3, len(inventory_data)))
    selected_pharmacies = random.sample(inventory_data, num_pharmacies)

    for pharmacy in selected_pharmacies:
        results.append(
            {
                "pharmacy_name": pharmacy.get("name"),
                "address": pharmacy.get("address"),
                "product": medicine_name,
                "price": round(random.uniform(10.0, 150.0), 2),
                "inventory": random.randint(0, 10),
            }
        )

    return results


root_agent = Agent(
    model="gemini-2.5-flash",
    name="inventory_agent",
    description="An agent that can check medicine inventory and prices across different pharmacies.",
    instruction="""
    You are an inventory agent. Your goal is to help users find medicine products in various pharmacies.
    When a user asks for a medicine, use the find_medicine tool to get a list of pharmacies that have it, along with the price and inventory levels.
    """,
    tools=[find_medicine],
)
