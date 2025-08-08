import difflib
import idna
from homoglyph_app.core.homoglyph_data import CANONICAL_MAP

def detect_homoglyphs(domain: str, known_legit_domain: str = None) -> dict:
    """
    Detects homoglyphs in a domain and reports suspicious characters.
    This version includes Punycode decoding, case normalization, and optional
    comparison against a known legitimate domain for a more accurate analysis.
    """
    try:
        # 1. Decode punycode if present (e.g., 'xn--...' -> Unicode)
        domain_unicode = idna.decode(domain)
    except idna.IDNAError:
        # If it's not a valid punycode string, use the original domain.
        domain_unicode = domain

    # 2. Normalize case (domains are case-insensitive)
    domain_lower = domain_unicode.lower()

    # 3. Canonical mapping replacement using our pre-built map.
    normalized_domain = "".join([CANONICAL_MAP.get(ch, ch) for ch in domain_lower])

    # 4. Determine if the domain is suspicious.
    is_suspicious = (domain_lower != normalized_domain)

    suspicious_chars_found = []
    if is_suspicious:
        # Use zip for a safe, parallel iteration.
        for orig_char, norm_char in zip(domain_lower, normalized_domain):
            if orig_char != norm_char:
                suspicious_chars_found.append({
                    'original': orig_char,
                    'canonical': norm_char,
                    'codepoint': f'U+{ord(orig_char):04X}'
                })

    # 5. Calculate a more meaningful similarity score.
    # If a known target is provided, use it. Otherwise, fall back to the normalized domain.
    if known_legit_domain:
        target = known_legit_domain.lower()
    else:
        target = normalized_domain

    similarity_score = difflib.SequenceMatcher(None, domain_lower, target).ratio()

    return {
        'is_suspicious': is_suspicious,
        'input_domain': domain_unicode, # Return the nice Unicode version
        'normalized_domain': normalized_domain,
        'similarity_score': f"{similarity_score:.0%}",
        'suspicious_chars': suspicious_chars_found
    }


