import os

# These dictionaries will be populated at startup and will hold our master lists.
# They will be imported and used by our detector and generator utilities.
HOMOGLYPH_MAP = {}
CANONICAL_MAP = {}

def load_data_from_file():
    """
    Parses char_codes.txt once at startup.
    It reads the hex codes, converts them to characters, and populates two
    master dictionaries for instant lookups later.
    """
    # Ensure we are using the global variables to populate them.
    global HOMOGLYPH_MAP, CANONICAL_MAP

    # Build a reliable path to the data file, starting from this file's location.
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'char_codes.txt')

    print("INFO:    Loading homoglyph data from:", file_path)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Ignore comments and empty lines
                if line.startswith('#') or not line.strip():
                    continue

                # Split the line by commas to get the hex codes
                codes = line.strip().split(',')
                
                # Convert all hex codes to actual characters, handling potential errors
                characters = []
                for code in codes:
                    try:
                        # Convert hex string (base 16) to an integer, then to a character
                        characters.append(chr(int(code.strip(), 16)))
                    except ValueError:
                        # Log an error if a code is malformed, but don't crash.
                        print(f"WARNING: Skipping malformed hex code '{code}' in data file.")
                        continue
                
                if not characters:
                    continue

                # The first character on the line is the "canonical" representation
                canonical_char = characters[0]

                # Populate our two master maps
                for char in characters:
                    # Map every character back to its canonical form (for the detector)
                    CANONICAL_MAP[char] = canonical_char
                    # Map every character to the full list of its siblings (for the generator)
                    HOMOGLYPH_MAP[char] = characters

        print("INFO:    Homoglyph data loaded successfully.")
    
    except FileNotFoundError:
        print("ERROR:   The data file 'char_codes.txt' was not found!")
        print("ERROR:   Please ensure the file exists at:", file_path)
        # We raise an exception to stop the server from starting without its data.
        raise