import re
from collections import Counter
from pathlib import Path
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.contrib import messages
from .forms import ArchivoForm
from .models import Archivo

TOKENIZER = re.compile(r"[\wáéíóúüñ]+", re.IGNORECASE)

def index(request):
    archivos = Archivo.objects.order_by("-subido_en")
    form = ArchivoForm()
    return render(request, "analisis/index.html", {"form": form, "archivos": archivos})

def subir_archivo(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Método no permitido")
    form = ArchivoForm(request.POST, request.FILES)
    if form.is_valid():
        obj = form.save()
        messages.success(request, "Archivo subido correctamente.")
        return redirect("index")
    else:
        archivos = Archivo.objects.order_by("-subido_en")
        return render(request, "analisis/index.html", {"form": form, "archivos": archivos})

def generar_histograma(request, pk):
    archivo = get_object_or_404(Archivo, pk=pk)
    ruta = Path(archivo.archivo.path)
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            texto = f.read()
    except UnicodeDecodeError:
        with open(ruta, "r", encoding="latin-1") as f:
            texto = f.read()

    palabras = TOKENIZER.findall(texto.lower())
    conteo = Counter(palabras)

    # Ordenar por frecuencia desc y alfabéticamente
    filas = sorted(conteo.items(), key=lambda kv: (-kv[1], kv[0]))

    return render(request, "analisis/histograma_tabla.html", {
    "archivo": archivo,
    "filas": filas,
    "total_palabras": sum(conteo.values()),
    "palabras_unicas": len(conteo),
})



from django.conf import settings
from django.contrib import messages
from django import forms
import os, collections, re
from django.urls import reverse

class UploadForm(forms.Form):
    file = forms.FileField(label="Archivo (.txt o .csv)")

LAST_UPLOAD_PATH = os.path.join(settings.MEDIA_ROOT, "uploads", "last.txt")

def handle_upload(f):
    os.makedirs(os.path.join(settings.MEDIA_ROOT, "uploads"), exist_ok=True)
    with open(LAST_UPLOAD_PATH, "wb") as dest:
        for chunk in f.chunks():
            dest.write(chunk)
    return LAST_UPLOAD_PATH

def index(request):
    return render(request, "analisis/index.html")

def upload(request):
    last_file = LAST_UPLOAD_PATH if os.path.exists(LAST_UPLOAD_PATH) else None
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            saved = handle_upload(form.cleaned_data["file"])
            messages.success(request, "Archivo subido correctamente.")
            return redirect(reverse("analisis:histograma"))
    else:
        form = UploadForm()
    ctx = {"form": form, "last_file": last_file}
    return render(request, "analisis/upload.html", ctx)

def histograma(request):
    # Lee el último archivo subido si existe y genera datos
    if not os.path.exists(LAST_UPLOAD_PATH):
        return render(request, "analisis/histograma_tabla.html", {"tabla": None, "grafico_url": None})

    with open(LAST_UPLOAD_PATH, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    # Tokenización muy básica
    tokens = re.findall(r"[\wáéíóúñÁÉÍÓÚÑ]+", text.lower())
    stop = {"de","la","que","el","en","y","a","los","del","se","las","por","un","para","con","no","una","su","al","lo","como","más","pero","sus","le","ya","o","esta","sí","porque","esta","entre"}
    tokens = [t for t in tokens if t not in stop and len(t) > 2]

    counter = collections.Counter(tokens)
    tabla = counter.most_common(30)

    # No generamos imagen aquí para simplificar; tu template mostrará la tabla
    return render(request, "analisis/histograma_tabla.html", {"tabla": tabla, "grafico_url": None})
