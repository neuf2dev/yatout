from django import forms
from .models import Annonce

class AnnonceForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = ['type_annonce', 'titre', 'categorie', 'prix', 'description', 'ville', 'telephone', 'image']
        widgets = {
            'type_annonce': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded p-2 text-sm bg-white font-bold text-[#1e40af]'
            }),
            'titre': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded p-2 text-sm', 'placeholder': 'Ex: Vends vélo de course'}),
            'categorie': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded p-2 text-sm bg-white'}),
            'prix': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded p-2 text-sm', 'placeholder': '0.00'}),
            'description': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded p-2 text-sm h-32', 'placeholder': 'Décrivez votre bien ou votre recherche...'}),
            'ville': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded p-2 text-sm', 'placeholder': 'Ex: Paris 11e'}),
            'telephone': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded p-2 text-sm', 'placeholder': 'Optionnel'}),
            'image': forms.FileInput(attrs={'class': 'w-full text-sm text-gray-500'}),
        }