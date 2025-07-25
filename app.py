# Importamos librerias
from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import os

# Suprimir warnings de TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Creamos nuestra funcion de dibujo
mpDibujo = mp.solutions.drawing_utils
ConfDibu = mpDibujo.DrawingSpec(thickness=1, circle_radius=1)

# Creamos un objeto donde almacenaremos la malla facial
mpMallaFacial = mp.solutions.face_mesh

# Creamos la app
app = Flask(__name__)

# Variable global para la cámara
camera = None

def init_camera():
    """Inicializar la cámara de forma segura"""
    global camera
    if camera is None or not camera.isOpened():
        # Probar diferentes índices de cámara
        for i in range(3):
            camera = cv2.VideoCapture(i)
            if camera.isOpened():
                print(f"Cámara encontrada en índice {i}")
                # Configurar propiedades de la cámara
                camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                camera.set(cv2.CAP_PROP_FPS, 30)
                break
        else:
            # Si no se encuentra cámara, usar índice 0 por defecto
            print("Usando cámara por defecto (índice 0)")
            camera = cv2.VideoCapture(0)
    return camera

def gen_frame():
    """Generar frames para streaming"""
    global camera
    
    # Inicializar la malla facial dentro de la función
    MallaFacial = mpMallaFacial.FaceMesh(max_num_faces=1)
    
    try:
        # Inicializar cámara
        camera = init_camera()
        
        while True:
            # Leemos la VideoCaptura
            ret, frame = camera.read()

            # Si tenemos un error
            if not ret:
                print("No se pudo leer el frame de la cámara")
                break
            else:
                # Correccion de color
                frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Observamos los resultados
                resultados = MallaFacial.process(frameRGB)

                # Si tenemos rostros
                if resultados.multi_face_landmarks:
                    # Iteramos
                    for rostros in resultados.multi_face_landmarks:
                        # Dibujamos
                        mpDibujo.draw_landmarks(frame, rostros, mpMallaFacial.FACEMESH_TESSELATION, ConfDibu, ConfDibu)

                # Codificamos nuestro video en Bytes
                suc, encode = cv2.imencode('.jpg', frame)
                if not suc:
                    continue
                frame_bytes = encode.tobytes()

                yield(b'--frame\r\n'
                      b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                      
    except Exception as e:
        print(f"Error en generación de frames: {e}")
    finally:
        # Liberar recursos
        if 'MallaFacial' in locals():
            del MallaFacial

# Ruta de aplicacion 'principal'
@app.route('/')
def index():
    return render_template('index.html')  # Minúscula

# Ruta del video
@app.route('/video')
def video():
    return Response(gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Liberar cámara al cerrar la aplicación
@app.teardown_appcontext
def cleanup_camera(error):
    global camera
    if camera is not None:
        camera.release()
        print("Cámara liberada")

# Manejar cierre forzado
import atexit

def cleanup_at_exit():
    global camera
    if camera is not None:
        camera.release()
        print("Cámara liberada al salir")

atexit.register(cleanup_at_exit)

# Ejecutamos la app
if __name__ == "__main__":
    print("🚀 Iniciando aplicación de detección facial...")
    print("🌐 Accede a: http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)