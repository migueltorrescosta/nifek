from django.contrib import admin
from magiclink.models import MagicLinkUnsubscribe, MagicLink

admin.site.register(MagicLink)
admin.site.register(MagicLinkUnsubscribe)
