
# 🛠 Manual de Usuario – Sistema Buscador de Productos Financieros

Este proyecto es un sistema completo para consultar productos financieros (como cuentas de ahorro), compuesto por:

- Backend en Django (con base de datos en PostgreSQL)  
- Frontend en React  
- Script opcional de scraping con Selenium

---

## 📁 Estructura general del proyecto

```bash
proyectoGitHub/
├── buscadorBack/              # Backend en Django
│   ├── buscador/              # App principal
│   ├── data/                  # Archivos fuente .xls
│   ├── evaluacion/            # Scripts de evaluación
│   ├── llenarBaseDatos.py     # Script para poblar la base de datos
│   └── manage.py
├── buscadorFrontend/          # Frontend en React (Vite)
│   └── buscador-cuentas/
├── data/                      # Archivos .xls (duplicados para facilidad de acceso)
├── requirementsBackend.txt    # Requisitos del backend (Django)
├── requirementsWebScraping.txt # Requisitos para el scraper (opcional)
├── webScraping/
│   ├── arania.py              # Script principal de scraping
│   └── chromedriver-linux64   # Driver para Selenium
```
---

## ✅ Requisitos previos

- Python 3.8+  
- PostgreSQL instalado y corriendo  
- Node.js y npm instalados  
- (Opcional) Google Chrome instalado para scraping  
- Acceso a una terminal o consola  

---

## 🔧 1. Instalación de dependencias del backend

Dentro del proyecto clonado, asegúrate de estar en el entorno virtual (si usas uno) y ejecuta:

bash
pip install -r requirementsBackend.txt

---

## 🛠 2. Configurar base de datos en settings.py

Abre el archivo:

bash
buscadorBack/buscador/settings.py

Edita la sección DATABASES con tus credenciales de PostgreSQL:

python
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nombre_base_datos',
        'USER': 'usuario',
        'PASSWORD': 'contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
> 🔐 Asegúrate de que la base de datos ya exista antes de continuar.

---

## 🔁 3. Aplicar migraciones

Luego, dentro de la carpeta buscadorBack/, ejecuta:

bash
python manage.py makemigrations
python manage.py migrate

Esto creará las tablas necesarias en la base de datos.

---

## 🧩 4. Llenar la base de datos

Una vez configurada la base de datos y aplicadas las migraciones, ejecuta:

bash
python llenarBaseDatos.py

Este script insertará datos usando los archivos .xls contenidos en las carpetas data/.

---

## 🚀 5. Ejecutar el servidor Django

Inicia el backend con:

bash
python manage.py runserver

Accede en el navegador a: http://127.0.0.1:8000

---

## 🌐 6. Ejecutar el frontend en React

En una nueva terminal, ve al directorio del frontend:

bash
cd buscadorFrontend/buscador-cuentas
npm install        # Solo la primera vez
npm run dev        # (o npm start, según configuración)

Por defecto, estará disponible en http://localhost:5173

---

## 🕷️ 7. (Opcional) Ejecutar scraping con Selenium

Si deseas actualizar los datos automáticamente con scraping, sigue estos pasos:

a. Instala las dependencias del scraper

bash
pip install -r requirementsWebScraping.txt

b. Ejecuta el script

bash
cd webScraping/
python arania.py

> ⚠️ Asegúrate de tener chromedriver y Google Chrome instalados.

---

## 📝 Notas finales y buenas prácticas

- Siempre ejecuta migrate después de clonar o cambiar modelos.  
- Usa entornos virtuales para evitar conflictos de dependencias.  
- Si cambias modelos de Django:

bash
python manage.py makemigrations
python manage.py migrate

- No hardcodees credenciales: usa un archivo .env con python-decouple o django-environ.  
- Usa pip freeze > requirementsBackend.txt para actualizar dependencias.  
- No olvides agregar un .gitignore para excluir ambiente/, env/ y archivos .db, .log, .pyc, etc.

---
