from django.apps import AppConfig

class HomoglyphAppConfig(AppConfig):
    """
    Application configuration for the homoglyph_app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'homoglyph_app'

    def ready(self):
        """
        This method is called by Django when the application is fully loaded and ready.
        It is the ideal place to perform one-time initialization tasks, like
        loading our homoglyph data into memory.
        """
        # We import here to avoid potential circular import issues.
        from .core import homoglyph_data

        # Execute our data loading function.
        homoglyph_data.load_data_from_file()