from django.contrib import admin
from .models import Thesis, Property, Tag
from magiclink.models import MagicLinkUnsubscribe, MagicLink

admin.site.register(MagicLink)
admin.site.register(MagicLinkUnsubscribe)

admin.site.register(Thesis)
admin.site.register(Property)
admin.site.register(Tag)
