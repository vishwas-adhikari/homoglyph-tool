import os
import json

HOMOGLYPH_MAP = {}
CANONICAL_MAP = {}

def load_data_from_file():
    """mana
    Loads the pre-built, clean homoglyph_map.json file and populates
    the master dictionaries for the application to use.
    """
    global HOMOGLYPH_MAP, CANONICAL_MAP

    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'homoglyph_map.json')
    print("INFO:    Loading pre-built homoglyph map...")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Load the entire perfect map from the JSON file.
            structured_map = json.load(f)

        # Now, build the two master lists from this perfect map.
        for canonical_char, full_group in structured_map.items():
            # The HOMOGLYPH_MAP is easy: map every char in the group to the full group list.
            for char in full_group:
                HOMOGLYPH_MAP[char] = full_group
            
            # The CANONICAL_MAP is also easy: map every char in the group to the key.
            for char in full_group:
                CANONICAL_MAP[char] = canonical_char

        print("INFO:    Homoglyph maps built successfully from pre-compiled JSON.")

    except FileNotFoundError:
        print(f"ERROR: The data file 'homoglyph_map.json' was not found!")
        print(f"ERROR: Please run the 'build_map.py' script first to generate it.")
        raise
    except Exception as e:
        print(f"ERROR: Failed to load or parse homoglyph_map.json: {e}")
        raise