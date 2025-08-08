import difflib

# Import the pre-populated map. We now trust this map to be 100% correct.
from homoglyph_app.core.homoglyph_data import CANONICAL_MAP

def detect_homoglyphs(domain: str) -> dict:
    """
    Analyzes a domain to detect homoglyphs using a reliable canonical map.
    """
    normalized_domain = "".join([CANONICAL_MAP.get(char, char) for char in domain])
    is_suspicious = (domain != normalized_domain)
    
    suspicious_chars_found = []
    if is_suspicious:
        for i, original_char in enumerate(domain):
            normalized_char = normalized_domain[i]
            if original_char != normalized_char:
                suspicious_chars_found.append({
                    'original': original_char,
                    'canonical': normalized_char,
                    'codepoint': f'U+{ord(original_char):04X}'
                })

    similarity_score = difflib.SequenceMatcher(None, domain, normalized_domain).ratio()
    
    report = {
        'is_suspicious': is_suspicious,
        'input_domain': domain,
        'normalized_domain': normalized_domain,
        'similarity_score': f"{similarity_score:.0%}",
        'suspicious_chars': suspicious_chars_found
    }
    
    return report