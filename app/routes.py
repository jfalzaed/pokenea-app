from flask import Blueprint, jsonify, render_template
import random
import socket
from .models import POKENEAS
from .utils import get_image_url

# Definición del Blueprint principal
main = Blueprint('main', __name__)

def get_container_id():
    """Obtiene el ID (hostname) del contenedor Docker."""
    return socket.gethostname()


@main.route('/')
def home():
    """Ruta principal: redirige a la vista con imagen."""
    return pokenea_imagen()


@main.route('/pokenea/json')
def pokenea_json():
    """
    Retorna en formato JSON los datos básicos de un Pokenea aleatorio.
    Incluye el ID del contenedor para verificar el despliegue en Docker Swarm.
    """
    pokenea = random.choice(POKENEAS)
    return jsonify({
        'id': pokenea['id'],
        'nombre': pokenea['nombre'],
        'altura': pokenea['altura'],
        'habilidad': pokenea['habilidad'],
        'container_id': get_container_id()
    })


@main.route('/pokenea/imagen')
def pokenea_imagen():
    """
    Muestra una página HTML con la imagen y frase filosófica de un Pokenea aleatorio.
    También incluye el ID del contenedor actual.
    """
    pokenea = random.choice(POKENEAS)
    image_url = get_image_url(pokenea['imagen'])
    
    return render_template(
        'pokenea.html',
        pokenea=pokenea,
        image_url=image_url,
        container_id=get_container_id()
    )
