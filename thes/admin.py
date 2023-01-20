from django.contrib import admin

from .models import Property, Tag, Thesis

admin.site.register(Thesis)
admin.site.register(Property)
admin.site.register(Tag)
