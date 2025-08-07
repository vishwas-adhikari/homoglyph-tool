from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
import json


# Import our detector and generator functions from the utils module
from .utils.detector import detect_homoglyphs
from .utils.generator import generate_homoglyphs
from .utils.shortener import shorten_url 

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
    


def shorten_api(request: HttpRequest):
    """
    API endpoint for handling URL shortening requests.
    Expects a POST request with a JSON body: {"url": "..."}
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

    try:
        data = json.loads(request.body)
        url = data.get('url')
        if not url:
            return JsonResponse({'error': 'Missing "url" key in request body'}, status=400)

        # Call our new shortener function
        shortened = shorten_url(url)
        
        response_data = {
            'original_url': url,
            'shortened_url': shortened
        }
        return JsonResponse(response_data)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)