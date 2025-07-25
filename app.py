import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from flask import Flask, render_template, Response
import cv2
import mediapipe as mp

# Configuración para Render
is_render = os.environ.get('RENDER', False)

app = Flask(__name__)

# Solo inicializar MediaPipe si no estamos en Render
if not is_render:
    mpDibujo = mp.solutions.drawing_utils
    ConfDibu = mpDibujo.DrawingSpec(thickness=1, circle_radius=1)
    mpMallaFacial = mp.solutions.face_mesh

camera = None

def init_camera():
    if is_render:
        return None
    # ... resto de tu código de cámara

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    if is_render:
        return "Streaming no disponible en Render (requiere cámara local)"
    # ... tu código de streaming

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)