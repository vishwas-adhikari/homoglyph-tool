import difflib

# Import the pre-populated map directly from the core data module.
# This map contains every confusable character and its "true" canonical version.
from homoglyph_app.core.homoglyph_data import CANONICAL_MAP

def detect_homoglyphs(domain: str) -> dict:
    """
    Analyzes a domain to detect homoglyphs and returns a detailed report.

    This function works by normalizing the input domain character by character
    using the pre-loaded CANONICAL_MAP. If the normalized version differs
    from the original, the domain is considered suspicious.

    Args:
        domain: The domain string to analyze.

    Returns:
        A dictionary containing the analysis report.
    """
    normalized_domain = ""
    suspicious_chars_found = []
    
    # Iterate through each character of the input domain
    for char in domain:
        # Look up the character in our master map.
        # If it's a normal character (like 'a'), it will map to itself.
        # If it's a homoglyph (like 'ɡ'), it will map to its canonical form ('g').
        # .get(char, char) ensures that if a character is not in the map, it defaults to itself.
        canonical_char = CANONICAL_MAP.get(char, char)
        normalized_domain += canonical_char
        
        # If the original character is different from its canonical version, it's a homoglyph.
        if char != canonical_char:
            suspicious_chars_found.append({
                'original': char,
                'canonical': canonical_char,
                'codepoint': f'U+{ord(char):04X}' # Provide the Unicode codepoint for clarity
            })

    # The domain is suspicious if the normalized version is not identical to the original.
    is_suspicious = (domain != normalized_domain)

    # Calculate a similarity score between the original and normalized domains.
    # This gives a sense of "how close" the spoof attempt is.
    similarity_score = difflib.SequenceMatcher(None, domain, normalized_domain).ratio()
    
    # Compile the final report.
    report = {
        'is_suspicious': is_suspicious,
        'input_domain': domain,
        'normalized_domain': normalized_domain,
        'similarity_score': f"{similarity_score:.0%}", # Format as a percentage
        'suspicious_chars': suspicious_chars_found
    }
    
    return report