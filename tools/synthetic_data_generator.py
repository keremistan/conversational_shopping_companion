import json
import random
import uuid
import os
from faker import Faker

fake = Faker()

class ShoppingDataGenerator:
    def __init__(self, schema_file):
        with open(schema_file, 'r') as f:
            self.schema = json.load(f)

    def _get_valid_val(self, field, d_type):
        """Generates realistic data based on the field name or type."""
        if field == "id": return str(uuid.uuid4())[:12]
        if field == "sku": return random.randint(10000, 99999)
        if field == "price": return round(random.uniform(1.99, 2999.99), 2)
        
        # Type-based fallbacks
        if d_type == "string":
            if "name" in field: return fake.ecommerce_name() if hasattr(fake, 'ecommerce_name') else f"{fake.color_name()} {fake.word().capitalize()}"
            if "brand" in field: return fake.company()
            if "category" in field: return random.choice(["Tech", "Home", "Fashion", "Pets", "Garden"])
            return fake.bs()
        if d_type == "int": return random.randint(1, 100)
        if d_type == "float": return round(random.uniform(0, 1), 2)
        return "Unknown"

    def _get_corrupted_val(self, d_type):
        """Generates data that breaks the schema rules."""
        pick = random.choice(["wrong_type", "null", "nonsense", "malformed_json"])
        if pick == "wrong_type": return "FREE" if d_type != "string" else 99999
        if pick == "null": return None
        if pick == "nonsense": return "---ERROR---"
        if pick == "malformed_json": return "{'broken':" # String that looks like bad JSON
        return ""

    def generate(self, filename, count, corruption_rate=0.1):
        """Streams generated data to a file."""
        print(f"Generating {count} entries to {filename}...")
        
        with open(filename, 'w') as f:
            for i in range(count):
                is_corrupt = random.random() < corruption_rate
                entry = {}
                
                for field, d_type in self.schema.items():
                    # Decide if this specific field should be the one to break
                    if is_corrupt and random.random() < 0.2:
                        entry[field] = self._get_corrupted_val(d_type)
                    else:
                        entry[field] = self._get_valid_val(field, d_type)
                
                # Randomly remove keys to simulate incomplete data
                if is_corrupt and random.random() < 0.1:
                    entry.pop(random.choice(list(entry.keys())))

                # Write as a single line (JSONL format is best for big data)
                f.write(json.dumps(entry) + "\n")
                
                if (i + 1) % 10000 == 0:
                    print(f"Progress: {i + 1}/{count}...")

# --- SETUP ---
# 1. Create your schema file (schema.json)
schema_content = {
    "id": "string",
    "name": "string",
    "price": "float",
    "brand": "string",
    "category": "string",
    "description": "string",
    "sku": "int",
    "merchant": "string"
}

schema_path = '../data_contracts/schemas/computer.json'

with open(schema_path, 'w') as f:
    json.dump(schema_content, f, indent=4)

# 2. Run the generator
gen = ShoppingDataGenerator(schema_path)
gen.generate('synthetic_shopping_data_xs.jsonl', count=1000, corruption_rate=0.15)
print("Done!")