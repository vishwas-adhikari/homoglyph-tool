from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
import json
from django.shortcuts import render, get_object_or_404 # Add get_object_or_404
from django.http import JsonResponse, HttpRequest, HttpResponseRedirect 


# Import our detector and generator functions from the utils module
from .utils.detector import detect_homoglyphs
from .utils.generator import generate_homoglyphs
from .utils.shortener import create_short_code # <-- Import our new function
from .models import ShortURL
 # <-- Import our new model

def index(request: HttpRequest):
    """
    Renders the main single-page application.
    """
    return render(request, 'homoglyph_app/index.html')


def detection_api(request: HttpRequest):
    """
    API endpoint for handling homoglyph detection requests.
    Expects a POST request with a JSON body: {"domain": "..."}
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

    try:
        data = json.loads(request.body)
        domain = data.get('domain')
        if domain is None:
            return JsonResponse({'error': 'Missing "domain" key in request body'}, status=400)

        # Call our detector function to get the analysis report
        report = detect_homoglyphs(domain)
        return JsonResponse(report)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)


def creation_api(request: HttpRequest):
    """
    API endpoint for handling homoglyph creation requests.
    Expects a POST request with a JSON body: {"domain": "..."}
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

    try:
        data = json.loads(request.body)
        domain = data.get('domain')
        if domain is None:
            return JsonResponse({'error': 'Missing "domain" key in request body'}, status=400)
        
        # Call our generator function to get a list of spoofed domains
        generated_domains = generate_homoglyphs(domain)
        return JsonResponse({'generated_domains': generated_domains})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
    


#new addition for shortener
def shorten_api(request: HttpRequest):
    """
    API endpoint for creating a new short URL in our own database.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

    try:
        data = json.loads(request.body)
        url_to_shorten = data.get('url')
        if not url_to_shorten:
            return JsonResponse({'error': 'Missing "url" key'}, status=400)
        
        # Generate a unique short code.
        short_code = create_short_code()

        # Prepend http:// if no protocol is specified, for consistency.
        if not url_to_shorten.startswith(('http://', 'https://')):
            url_to_shorten = f"http://{url_to_shorten}"

        # Create the new short URL record in the database.
        ShortURL.objects.create(
            original_url=url_to_shorten,
            short_code=short_code
        )
        
        # Build the full, clickable short URL to send back to the user.
        # We'll use a '/r/' prefix to keep redirect URLs separate.
        redirect_path = f"/r/{short_code}"
        full_short_url = request.build_absolute_uri(redirect_path)

        response_data = {
            'original_url': url_to_shorten,
            'shortened_url': full_short_url
        }
        return JsonResponse(response_data)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

def redirect_view(request: HttpRequest, short_code: str):
    """
    Looks up a short code and redirects the user to the original URL.
    """
    # Find the ShortURL object, or return a 404 Not Found error if it doesn't exist.
    short_url_object = get_object_or_404(ShortURL, short_code=short_code)
    
    # Redirect the user to the original URL.
    return HttpResponseRedirect(short_url_object.original_url)