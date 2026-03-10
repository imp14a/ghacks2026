
import json
import random

def generate_real_inventory():
    pharmacies = []
    pharmacy_chains = [
        "Farmacia San Pablo",
        "Farmacias del Ahorro",
        "Farmacias Benavides",
        "Farmacias Similares",
        "Farmacias YZA"
    ]
    medicines = [
        {"name": "Amoxicillin (500mg)", "price": 6.8},
        {"name": "Cefalexin (500mg)", "price": 6.0},
        {"name": "Doxycycline (100mg)", "price": 5.0},
        {"name": "Azithromycin (250mg)", "price": 8.2},
        {"name": "Ciprofloxacin (500mg)", "price": 130},
        {"name": "Metronidazole (500mg)", "price": 128},
        {"name": "Losartan (50mg)", "price": 4.4},
        {"name": "Carvedilol (12.5mg)", "price": 7.0},
        {"name": "Spironolactone (25mg)", "price": 6.0},
        {"name": "Amlodipine (5mg)", "price": 96},
        {"name": "Simvastatin (20mg)", "price": 102},
        {"name": "Linagliptin (5mg)", "price": 24},
        {"name": "Empagliflozin (25mg)", "price": 30},
        {"name": "Metformin (500mg)", "price": 92},
        {"name": "Omeprazole (20mg)", "price": 106},
        {"name": "Gabapentin (300mg)", "price": 140},
        {"name": "Sertraline (50mg)", "price": 156},
        {"name": "Sildenafil (Generic Viagra)", "price": 6.8},
        {"name": "Tadalafil (Generic Cialis)", "price": 184},
        {"name": "Paracetamol", "price": 50},
        {"name": "Ibuprofen", "price": 60},
        {"name": "Loratadine", "price": 70}
    ]

    for i in range(20):
        pharmacy_name = pharmacy_chains[i % len(pharmacy_chains)]
        pharmacy = {
            "name": pharmacy_name,
            "address": f"{i+1} Main St, Mexico City",
            "branch_number": i+1,
            "products": []
        }
        
        # Ensure we have 20 products
        products_for_pharmacy = random.sample(medicines, 20)

        for product_info in products_for_pharmacy:
            product = {
                "name": product_info["name"],
                "inventory": random.randint(0, 100),
                "price": product_info["price"]
            }
            pharmacy["products"].append(product)
        pharmacies.append(pharmacy)

    with open("/usr/local/google/home/agusramirez/cloud/genai/gchacks2026/mpa_runtime/mpa/sub_agents/inventory_agent/mock_inventory.json", "w") as f:
        json.dump(pharmacies, f, indent=4)

if __name__ == "__main__":
    generate_real_inventory()
