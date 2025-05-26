from django import forms
from .models import Book  # ou Livre si tu as changé le nom

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['titre', 'description', 'fichier', 'version', 'categorie']
        # NE PAS mettre 'valide' ici !
