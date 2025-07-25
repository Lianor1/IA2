from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>¡Hola desde Flask en Render!</h1>
    <p>Tu aplicación está funcionando correctamente</p>
    <a href="/saludo/Mundo">Probar otra ruta</a>
    '''

@app.route('/saludo/<nombre>')
def saludo(nombre):
    return f'<h1>¡Hola {nombre}!</h1><p>Esta es tu app Flask en Render</p>'

# Importante para Render
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)