# PFG

Proyecto de fin de grado

# Descripción

La idea original parte de quantika14 basado en la herramienta Shodan.
Se basa en la extracción de toda la información posible de cierto host, para conseguir
encontrar las vulnerabilidades y que posteriormente puedan ser explotadas.

# Estructura

# - Cement -

Es el framework que se utiliza para la creación de los bots de rastreo. Está basado en
python y facilita la ejecución por línea de comandos (CLI).

# - Flask -

Está basado en python y se usará para la creación de la API (Backend).

Para iniciar el backend en local:
$ source venv/bin/activate (venv)
$ export FLASK_APP=flasky.py (venv)
$ pip install -r requirements.txt
$ flask run

# - Vue -

Vue.js se utilizará para la creación de la parte del cliente (frontend).

Se deben instalar en primera instancia las librerias: \$ npm install

# - Docker -

Para poder utilizar el proyecto sin ningún problema en cuanto al sistema operativo y ajustes
generales, se utilizaran contenedores docker.
