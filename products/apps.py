from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    
    #when the app runs it compares the app state with the given condition in signals
    def ready(self):
        import products.signals