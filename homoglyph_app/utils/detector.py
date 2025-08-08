import difflib
import unicodedata

from homoglyph_app.core.homoglyph_data import CANONICAL_MAP

# List of invisible characters to be removed.
ZERO_WIDTH_CHARS = [
    "\u200B",  # Zero Width Space
    "\u200C",  # Zero Width Non-Joiner
    "\u200D",  # Zero Width Joiner
    "\uFEFF",  # Zero Width No-Break Space
    "\u00AD",  # Soft Hyphen
]

def detect_homoglyphs(domain: str) -> dict:
    """
    Detects homoglyphs using a multi-stage cleaning and normalization process
    to handle a wide range of obfuscation techniques.
    """
    original_input = domain

    # --- STAGE 1: Aggressive Compatibility Normalization (NFKC) ---
    # This is the most important step. It handles a huge range of tricks:
    # - It separates characters from their combining marks (like accents) and often discards the marks.
    # - It converts many lookalike characters to their simple ASCII equivalents.
    # - It changes characters like 'ﬁ' into 'f' and 'i'.
    # Example: 'n' + '`' (U+0300) -> 'n'
    # Example: 'ɡ' (U+0261) -> 'g'
    normalized_form = unicodedata.normalize('NFKC', domain)
    
    # --- STAGE 2: Remove Invisible Characters ---
    # After normalization, we strip out any remaining zero-width characters.
    for zw in ZERO_WIDTH_CHARS:
        normalized_form = normalized_form.replace(zw, "")

    # --- STAGE 3: Final Canonical Mapping ---
    # We run our custom canonical map on the already-normalized string.
    # This handles any homoglyphs that NFKC didn't catch (e.g., Cyrillic 'а' -> Latin 'a').
    final_canonical_domain = "".join([CANONICAL_MAP.get(char, char) for char in normalized_form])
    
    # --- The Final Decision ---
    # We compare the fully cleaned string to the original input.
    # We also lowercase both to ensure the comparison is case-insensitive.
    is_suspicious = (final_canonical_domain.lower() != original_input.lower())

    suspicious_chars_found = []
    if is_suspicious:
        # For reporting, we can show the difference between the NFKC form and the final canonical form.
        # This gives a clearer indication of what was changed.
        for i in range(min(len(normalized_form), len(final_canonical_domain))):
            if normalized_form[i] != final_canonical_domain[i]:
                suspicious_chars_found.append({
                    'original': normalized_form[i],
                    'canonical': final_canonical_domain[i],
                    'codepoint': f'U+{ord(normalized_form[i]):04X}'
                })
    
    similarity_score = difflib.SequenceMatcher(None, original_input, final_canonical_domain).ratio()

    return {
        'is_suspicious': is_suspicious,
        'input_domain': original_input,
        'normalized_domain': final_canonical_domain,
        'similarity_score': f"{similarity_score:.0%}",
        'suspicious_chars': suspicious_chars_found
    }