import random
import string

# Import our new database model.
from homoglyph_app.models import ShortURL

# Define the character set for our short codes.
CHARS = string.ascii_letters + string.digits
CODE_LENGTH = 6 # We can make our codes 6 characters long.

def create_short_code() -> str:
    """
    Generates a unique, random short code of a specified length.

    This function includes a loop to ensure that the generated code
    does not already exist in the database, preventing collisions.

    Returns:
        A unique short code string.
    """
    while True:
        # Generate a random string of the specified length.
        short_code = "".join(random.choices(CHARS, k=CODE_LENGTH))
        
        # Check if a ShortURL object with this code already exists.
        if not ShortURL.objects.filter(short_code=short_code).exists():
            # If it doesn't exist, we've found a unique code.
            return short_code