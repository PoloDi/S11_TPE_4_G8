
"""
UNEMI — S11-TPE_4: Seguridad Informática
Aplicación Web VULNERABLE a Inyección SQL
NO usar en entornos de producción
"""

from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Inicializar base de datos con datos de prueba
def init_db():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT
        )
    ''')
    # Insertar usuarios de prueba
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'Admin123!', 'admin@empresa.ec')")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (2, 'usuario1', 'ClaveSegura2026', 'juan@empresa.ec')")
    conn.commit()
    conn.close()

# Plantilla del formulario
FORMULARIO = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Práctica SQLi — Inicio de Sesión</title>
    <style>body{font-family:sans-serif;max-width:400px;margin:2rem auto;padding:2rem;box-shadow:0 0 10px #ccc;}</style>
</head>
<body>
    <h2>Inicio de Sesión — Sistema Vulnerable</h2>
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

        # ⚠ VULNERABILIDAD: Concatenación directa en consulta SQL
        consulta = f"SELECT * FROM users WHERE username = '{usuario}' AND password = '{clave}'"
        print(f"[DEBUG] Consulta ejecutada: {consulta}")

        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        resultado = cursor.execute(consulta).fetchone()
        conn.close()

        if resultado:
            return render_template_string(FORMULARIO, mensaje=f"✅ Acceso CONCEDIDO. Bienvenido: {resultado[1]}")
        else:
            return render_template_string(FORMULARIO, mensaje="❌ Credenciales inválidas")

    return render_template_string(FORMULARIO)

if __name__ == '__main__':
    init_db()
    print("[INFO] Base de datos inicializada")
    print("[INFO] Servidor vulnerable en http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
