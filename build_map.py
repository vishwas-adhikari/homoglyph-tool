import json

# The path to our source data and the path for our clean output file.
SOURCE_FILE = 'homoglyph_app/data/char_codes.txt'
OUTPUT_FILE = 'homoglyph_app/data/homoglyph_map.json'

# --- The Source of Truth ---
# This set contains all characters we consider standard and "safe".
SAFE_ASCII_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-.")

def create_perfect_map():
    """
    Reads the raw char_codes.txt file and generates a clean, reliable
    JSON map for our Django application to use.
    """
    print(f"Reading raw data from {SOURCE_FILE}...")
    
    # This dictionary will hold our perfectly structured data.
    # The key will be the "safe" character, and the value will be the list of all its lookalikes.
    # e.g., { "a": ["a", "а", "ɑ"], "b": ["b", "Ь"], ... }
    structured_map = {}

    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue

                codes = line.strip().split(',')
                group = []
                for code in codes:
                    try:
                        group.append(chr(int(code.strip(), 16)))
                    except ValueError:
                        continue
                
                if not group:
                    continue

                # Find the single "safe" ASCII character in this group to use as the key.
                safe_key = None
                for char in group:
                    if char in SAFE_ASCII_CHARS:
                        safe_key = char
                        break
                
                # If we found a safe key (like 'a', 'b', 'c', etc.)...
                if safe_key:
                    # Add it to our structured map.
                    structured_map[safe_key] = group

        print(f"Successfully processed {len(structured_map)} character groups.")

        # Write the clean, structured map to our output JSON file.
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(structured_map, f, ensure_ascii=False, indent=2)

        print(f"Success! Perfect mapping has been written to {OUTPUT_FILE}")

    except FileNotFoundError:
        print(f"ERROR: Source file not found at {SOURCE_FILE}. Make sure the path is correct.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    create_perfect_map()