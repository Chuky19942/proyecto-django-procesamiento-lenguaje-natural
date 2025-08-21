# Sistema PLN (Django + Pipenv)

Entregables listos según la solicitud.

## Requisitos
- Python 3.11+
- pipenv

## Instalación y ejecución

```bash
cd sistema_pln
pipenv install
pipenv run python manage.py migrate
pipenv run python manage.py createsuperuser  # crea tu usuario admin
pipenv run python manage.py runserver
```

Luego visita: http://127.0.0.1:8000/

## Funcionalidad
- Subir archivos **.txt** y guardarlos en el servidor (carpeta `media/archivos/`).
- En la página de inicio verás la lista de archivos subidos.
- Botón “Generar histograma” que procesa el archivo y **muestra la frecuencia de palabras en una tabla**.
- **Admin de Django** habilitado en `/admin/`.
- Configuración en **español** y zona horaria **America/Mexico_City**.

## Estructura
- App: `analisis`
- Modelo: `Archivo` (FileField)
- Vistas: `index`, `subir_archivo`, `generar_histograma`
- Plantillas en `templates/` con Pico.css para una UI simple.

## Colaboración en GitHub
Para agregar al usuario **nerfeMats** como colaborador:
1. Sube este proyecto a un repositorio de GitHub.
2. Ve a **Settings → Collaborators & teams**.
3. Haz clic en **Add people** e invita a `nerfeMats` con el rol que desees (por ejemplo *Write*).
4. La persona debe aceptar la invitación.

> Si prefieres hacerlo por CLI:
```bash
gh repo create tu-usuario/sistema_pln --public --source=. --remote=origin
git push -u origin main
gh repo add-collaborator nerfeMats --permission write
```
(Usa la GitHub CLI `gh`, iniciando sesión con `gh auth login`).

## Notas
- Acepta únicamente archivos `.txt` hasta 5 MB.
- Para usar archivos en producción, configura `DEBUG=False` y un servidor de archivos estáticos y media.
