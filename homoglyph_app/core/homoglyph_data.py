import os

# --- The Source of Truth ---
# This set contains all characters we consider standard and "safe".
SAFE_ASCII_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-.")

# --- Global Dictionaries ---
# These will be populated by our new, robust loading logic.
HOMOGLYPH_MAP = {}
CANONICAL_MAP = {}

def load_data_from_file():
    """
    Parses char_codes.txt with a robust, two-pass strategy to ensure
    the canonical map is always correct, regardless of the data file's structure.
    """
    global HOMOGLYPH_MAP, CANONICAL_MAP

    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'char_codes.txt')
    print("INFO:    Loading homoglyph data with new ROBUST strategy...")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            all_lines_as_chars = []
            
            # --- Pass 1: Read all data into memory ---
            # Convert all hex codes to characters for easier processing.
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                codes = line.strip().split(',')
                characters = []
                for code in codes:
                    try:
                        characters.append(chr(int(code.strip(), 16)))
                    except ValueError:
                        continue
                if characters:
                    all_lines_as_chars.append(characters)

            # --- Pass 2: Build the Perfect Canonical Map ---
            # This is the most critical part of the logic.
            
            # First, map every safe character to itself. This is the default.
            for char in SAFE_ASCII_CHARS:
                CANONICAL_MAP[char] = char
            
            # Now, for each homoglyph group from the file...
            for group in all_lines_as_chars:
                # Find the single "safe" character in this group, if one exists.
                safe_char_in_group = None
                for char in group:
                    if char in SAFE_ASCII_CHARS:
                        safe_char_in_group = char
                        break
                
                # If we found a safe character (e.g., 'o' in a group with 'о', 'ο')...
                if safe_char_in_group:
                    # Map all OTHER (unsafe) characters in that group to this one safe character.
                    for char in group:
                        if char != safe_char_in_group:
                            CANONICAL_MAP[char] = safe_char_in_group
            
            # --- Pass 3: Build the Homoglyph Map (for the Generator) ---
            # This part can remain simple.
            for group in all_lines_as_chars:
                for char in group:
                    HOMOGLYPH_MAP[char] = group

        print("INFO:    Homoglyph data loaded successfully.")
    
    except FileNotFoundError:
        print("ERROR:   The data file 'char_codes.txt' was not found!")
        raise