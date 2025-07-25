from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/saludo/<nombre>')
def saludo(nombre):
    return f'''
    <div style="text-align: center; margin-top: 50px;">
        <h1>¡Hola {nombre}!</h1>
        <p>Esta es tu app Flask en Render</p>
        <a href="/" class="btn btn-primary">Volver al inicio</a>
    </div>
    '''

# Importante para Render
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)