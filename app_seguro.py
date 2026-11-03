from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('usuarios_seguro.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'Admin123!', 'admin@empresa.ec')")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (2, 'usuario1', 'ClaveSegura2026', 'juan@empresa.ec')")
    conn.commit()
    conn.close()

FORMULARIO = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Práctica SQLi — Versión Segura</title>
    <style>body{font-family:sans-serif;max-width:400px;margin:2rem auto;padding:2rem;box-shadow:0 0 10px #ccc;}</style>
</head>
<body>
    <h2>Inicio de Sesión — Sistema PROTEGIDO</h2>
    <form method="POST">
        <label>Usuario:</label><br>
        <input type="text" name="username" required><br><br>
        <label>Contraseña:</label><br>
        <input type="password" name="password" required><br><br>
        <input type="submit" value="Ingresar">
    </form>
    {% if mensaje %}<p><strong>{{ mensaje }}</strong></p>{% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        clave = request.form['password']

        # ✅ MITIGACIÓN: Consulta parametrizada (sentencia preparada)
        consulta = "SELECT * FROM users WHERE username = ? AND password = ?"
        parametros = (usuario, clave)

        conn = sqlite3.connect('usuarios_seguro.db')
        cursor = conn.cursor()
        resultado = cursor.execute(consulta, parametros).fetchone()
        conn.close()

        if resultado:
            return render_template_string(FORMULARIO, mensaje=f"✅ Acceso CONCEDIDO. Bienvenido: {resultado[1]}")
        else:
            return render_template_string(FORMULARIO, mensaje="❌ Credenciales inválidas — intento de inyección bloqueado")

    return render_template_string(FORMULARIO)

if __name__ == '__main__':
    init_db()
    print("[INFO] Base de datos inicializada")
    print("[INFO] Servidor SEGURO en http://127.0.0.1:5001")
    app.run(debug=True, port=5001)
