from django.contrib import admin
from .models import Card, Collection, UserCardScore

admin.site.register(Card)
admin.site.register(Collection)
admin.site.register(UserCardScore)
