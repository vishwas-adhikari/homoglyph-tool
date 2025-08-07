import requests

# The endpoint for the TinyURL API is simple and direct.
TINYURL_API_ENDPOINT = "http://tinyurl.com/api-create.php"

def shorten_url(url_to_shorten: str) -> str:
    """
    Shortens a given URL using the TinyURL API.

    Args:
        url_to_shorten: The full URL string that needs to be shortened.

    Returns:
        The shortened URL string, or an error message if the process fails.
    """
    if not url_to_shorten.startswith(('http://', 'https://')):
        # Prepend http:// if no protocol is specified, as the API requires it.
        url_to_shorten = f"http://{url_to_shorten}"

    try:
        # The API is called by passing the URL as a GET parameter.
        response = requests.get(TINYURL_API_ENDPOINT, params={'url': url_to_shorten})
        
        # Raise an exception if the API returns an error status (like 4xx or 5xx).
        response.raise_for_status()
        
        # The shortened URL is returned in the response body as plain text.
        return response.text

    except requests.RequestException as e:
        # Handle potential network errors, timeouts, or bad responses from the API.
        print(f"ERROR: Could not connect to TinyURL API. {e}")
        return "Error: Could not shorten URL."