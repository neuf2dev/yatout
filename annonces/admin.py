from django.contrib import admin
from .models import Annonce

@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'prix', 'ville', 'date_publication')