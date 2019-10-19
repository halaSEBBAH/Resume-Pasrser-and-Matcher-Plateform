from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Cv
from .forms import CVForm
from Applicant_Tracking_System.scripts.Extraction import *
import requests


# Create your views here.

def index(request):
    context = {}
    if request.POST.get('test') is None:
        test = ''
    else:
        txt = request.POST.get('test')
        condidatActuel = Condidat()
        condidatActuel.Extractor(txt)
        context = {
            'email': '-'.join(condidatActuel.email),
            'url': '-'.join(condidatActuel.url),
            'name': '-'.join(condidatActuel.name),
            'phone': '-'.join(condidatActuel.mobile)
        }
    # return render(request, 'SubmitFrom/index.html', {'test': test})


    return render(request, 'afficheur/cvResult.html', context)

