import json
import os
from google.adk.agents.llm_agent import Agent

# Get the directory of the current file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MOCK_INVENTORY_PATH = os.path.join(CURRENT_DIR, 'mock_inventory.json')

def find_medicine(medicine_name: str):
    """
    Searches for a medicine product in the mock inventory and returns pharmacies that have it.
    
    Args:
        medicine_name: The name of the medicine to search for (e.g., 'Paracetamol', 'Ibuprofen').
        
    Returns:
        A list of pharmacy objects containing the found medicine product, its price and inventory.
    """
    try:
        if not os.path.exists(MOCK_INVENTORY_PATH):
             # Try absolute path if relative fails in some environments
             potential_path = '/Users/ososa/Developer/ghacks2026/mpa_runtime/mpa/sub_agents/inventory_agent/mock_inventory.json'
             if os.path.exists(potential_path):
                 path_to_use = potential_path
             else:
                 return {"error": f"Mock inventory file not found at {MOCK_INVENTORY_PATH}"}
        else:
            path_to_use = MOCK_INVENTORY_PATH

        with open(path_to_use, 'r') as f:
            inventory_data = json.load(f)
    except Exception as e:
        return {"error": str(e)}

    results = []
    # Normalize query for better matching
    query = medicine_name.lower()
    
    for pharmacy in inventory_data:
        for product in pharmacy.get('products', []):
            # Check if query is in product name
            if query in product.get('name', '').lower():
                results.append({
                    "pharmacy_name": pharmacy.get('name'),
                    "address": pharmacy.get('address'),
                    "product": product.get('name'),
                    "price": product.get('price'),
                    "inventory": product.get('inventory')
                })
    
    return results

root_agent = Agent(
    model='gemini-2.5-flash',
    name='inventory_agent',
    description='An agent that can check medicine inventory and prices across different pharmacies.',
    instruction='''You are an inventory agent. Your goal is to help users find medicine products in various pharmacies.
    When a user asks for a medicine, use the find_medicine tool to get a list of pharmacies that have it, along with the price and inventory levels.
    You MUST return the results as a JSON array of objects. Each object should have:
    - pharmacy_name: Name of the pharmacy
    - address: Address of the pharmacy
    - product: Name of the found medicine product
    - price: Price of the product
    - inventory: Current stock level
    
    Example output format:
    [
      {"pharmacy_name": "...", "address": "...", "product": "...", "price": ..., "inventory": ...},
      ...
    ]
    
    If no products match, return an empty array [].''',
    tools=[find_medicine],
)
