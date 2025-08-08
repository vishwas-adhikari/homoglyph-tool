import random
from homoglyph_app.core.homoglyph_data import HOMOGLYPH_MAP

def generate_homoglyphs(domain: str, max_results: int = 20) -> list:
    if not domain:
        return []

    # Step 1: Strip common prefixes
    prefixes = ["https://", "http://", "www."]
    prefix = ""
    for p in prefixes:
        if domain.startswith(p):
            prefix = p
            domain = domain[len(p):]
            break

    # Step 2: Separate the main domain and TLD
    if "." in domain:
        main_part, tld = domain.rsplit(".", 1)  # split only on last '.'
    else:
        main_part, tld = domain, ""

    generated_domains = set()

    while len(generated_domains) < max_results:
        new_domain_list = list(main_part)

        # Step 3: Identify replaceable positions in main domain only
        replaceable_indices = [
            i for i, char in enumerate(new_domain_list)
            if char in HOMOGLYPH_MAP and len(HOMOGLYPH_MAP[char]) > 1
        ]

        if not replaceable_indices:
            break

        # Step 4: Randomly choose 1 or 2 positions to replace
        num_changes = random.choice([1, 2])
        chosen_indices = random.sample(replaceable_indices, min(num_changes, len(replaceable_indices)))

        for i in chosen_indices:
            homoglyph_choices = [hg for hg in HOMOGLYPH_MAP[new_domain_list[i]] if hg != new_domain_list[i]]
            if homoglyph_choices:
                new_domain_list[i] = random.choice(homoglyph_choices)

        # Step 5: Rebuild domain and add prefix + untouched TLD
        new_domain = "".join(new_domain_list)
        if tld:
            new_domain += "." + tld

        generated_domains.add(prefix + new_domain)

    return list(generated_domains)
