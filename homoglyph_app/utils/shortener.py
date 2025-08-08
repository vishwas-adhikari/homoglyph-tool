import requests
from urllib.parse import urlparse, urlunparse

TINYURL_API_ENDPOINT = "http://tinyurl.com/api-create.php"

def shorten_url(url_to_shorten: str) -> str:
    if not url_to_shorten.startswith(('http://', 'https://')):
        url_to_shorten = f"http://{url_to_shorten}"

    try:
        # Parse the URL into components
        parsed_url = urlparse(url_to_shorten)

        # Convert the hostname to punycode if it contains non-ASCII
        hostname_ascii = parsed_url.hostname.encode('idna').decode('ascii')

        # Rebuild the URL with ASCII hostname
        parsed_url = parsed_url._replace(netloc=hostname_ascii + (":" + str(parsed_url.port) if parsed_url.port else ""))
        ascii_url = urlunparse(parsed_url)

        # Send request to TinyURL API
        response = requests.get(TINYURL_API_ENDPOINT, params={'url': ascii_url})
        response.raise_for_status()
        
        return response.text

    except requests.RequestException as e:
        print(f"ERROR: Could not connect to TinyURL API. {e}")
        return "Error: Could not shorten URL."
    except Exception as e:
        print(f"ERROR: Invalid URL or encoding issue. {e}")
        return "Error: Could not shorten URL."
