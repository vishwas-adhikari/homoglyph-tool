from django.db import models

class ShortURL(models.Model):
    """
    A model to store the mapping between a short code and an original URL.
    """
    # The original, long URL that the user wants to shorten.
    original_url = models.URLField(max_length=2048)
    
    # The unique, randomly generated short code (e.g., 'aZ89bC').
    # We make it unique to prevent collisions.
    short_code = models.CharField(max_length=8, unique=True)
    
    # The date and time when the short URL was created.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.short_code} -> {self.original_url[:50]}'