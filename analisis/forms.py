from django import forms
from .models import Archivo

class ArchivoForm(forms.ModelForm):
    class Meta:
        model = Archivo
        fields = ["archivo", "nombre"]

    def clean_archivo(self):
        f = self.cleaned_data["archivo"]
        # Aceptar únicamente .txt
        if not f.name.lower().endswith(".txt"):
            raise forms.ValidationError("Solo se permiten archivos .txt")
        if f.size > 5 * 1024 * 1024:
            raise forms.ValidationError("El archivo no debe exceder 5 MB")
        return f
