import random

# Import the pre-populated map that contains every character and its "family" of lookalikes.
from homoglyph_app.core.homoglyph_data import HOMOGLYPH_MAP

def generate_homoglyphs(domain: str, max_results: int = 20) -> list:
    """
    Generates a list of visually similar domains using homoglyph replacements.

    Args:
        domain: The legitimate domain string to spoof.
        max_results: The maximum number of variants to generate.

    Returns:
        A list of generated homoglyph domains.
    """
    if not domain:
        return []

    generated_domains = set()
    domain_chars = list(domain)

    # Find all character positions in the domain that have known homoglyphs
    replaceable_indices = [
        i for i, char in enumerate(domain_chars) 
        if char in HOMOGLYPH_MAP and len(HOMOGLYPH_MAP[char]) > 1
    ]

    if not replaceable_indices:
        return [] # No characters in the domain can be replaced.

    # Generation Strategy 1: Replace one character at a time.
    # This creates the most common and believable spoofs.
    for index in replaceable_indices:
        original_char = domain_chars[index]
        # Iterate through all possible homoglyphs for that character
        for homoglyph in HOMOGLYPH_MAP[original_char]:
            if homoglyph == original_char:
                continue # Don't replace a character with itself

            new_domain_list = domain_chars[:]
            new_domain_list[index] = homoglyph
            generated_domains.add("".join(new_domain_list))

            if len(generated_domains) >= max_results:
                return list(generated_domains)

    # Generation Strategy 2: Create a few highly-spoofed domains with multiple replacements.
    # This adds variety. We'll try this a few times.
    for _ in range(5):
        if len(generated_domains) >= max_results:
            break
        
        temp_domain_list = domain_chars[:]
        # Pick a random number of characters to replace (at least 1)
        num_to_replace = random.randint(1, len(replaceable_indices))
        indices_to_replace = random.sample(replaceable_indices, num_to_replace)

        for index in indices_to_replace:
            original_char = temp_domain_list[index]
            # Pick a random homoglyph (that isn't the original character)
            replacement = random.choice([h for h in HOMOGLYPH_MAP[original_char] if h != original_char])
            temp_domain_list[index] = replacement
        
        generated_domains.add("".join(temp_domain_list))

    return list(generated_domains)