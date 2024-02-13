# admin.py
from django.contrib import admin
from django.apps import apps

# Get all models from the current app
app_models = apps.get_app_config("user").get_models()

# Register all models in the admin dashboard
for model in app_models:
    admin.site.register(model)
