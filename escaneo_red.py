"""
UNEMI — S11-TPE_4: Seguridad Informática
Módulo de Escaneo Ético de Red — Puertos y Servicios
Solo para uso en red autorizada / entorno de laboratorio
"""

import socket
from datetime import datetime

PUERTOS_COMUNES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 8080: "HTTP-Alt"
}

def escanear_puerto(host, puerto, tiempo_espera=0.5):
    """Verifica si un puerto está abierto"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(tiempo_espera)
            resultado = s.connect_ex((host, puerto))
            if resultado == 0:
                servicio = PUERTOS_COMUNES.get(puerto, "Desconocido")
                return True, servicio
            return False, None
    except Exception as e:
        return False, str(e)

def escanear_red(host_objetivo="127.0.0.1", rango_puertos=range(1, 1025)):
    """Escanear rango de puertos en el host indicado"""
    print("="*60)
    print(f"  ESCANEO DE RED — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Objetivo: {host_objetivo}")
    print(f"  Rango de puertos: {rango_puertos.start} - {rango_puertos.stop-1}")
    print("="*60)

    abiertos = []
    for puerto in rango_puertos:
        estado, servicio = escanear_puerto(host_objetivo, puerto)
        if estado:
            print(f"  [ABIERTO] Puerto {puerto:4d} → {servicio}")
            abiertos.append((puerto, servicio))

    if not abiertos:
        print("  No se encontraron puertos abiertos en el rango escaneado")

    print("\n" + "-"*60)
    print(f"  Total puertos abiertos: {len(abiertos)}")
    print("  Buenas prácticas:")
    print("  • Cerrar puertos innecesarios")
    print("  • Restringir acceso por cortafuegos")
    print("  • Usar cifrado en servicios expuestos")
    print("="*60)
    return abiertos

if __name__ == "__main__":
    # Escanear localhost y rango extendido
    escanear_red("127.0.0.1", range(1, 1000))
