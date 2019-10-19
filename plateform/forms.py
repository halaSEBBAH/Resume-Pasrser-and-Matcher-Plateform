from django.forms import ModelForm,TextInput

from .models import Cv

class CVForm(ModelForm):
    class Meta:
        model = Cv
        fields  = ['CvRaw']
        widgets = {'CvRaw': TextInput(attrs={'class': 'input', 'placeholder': 'Procced your resume'})}