from django.apps import apps
from django.contrib import admin

for model in apps.get_models():
    try:
        class modelAdmin(admin.ModelAdmin):
            list_display = [field.name for field in model._meta.fields]
        admin.site.register(model, modelAdmin)
    except admin.sites.AlreadyRegistered:
        pass
