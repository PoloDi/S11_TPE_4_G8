---

## ARCHIVO: `MANUAL_USO.md`

```markdown
# MANUAL DE USO Y PRUEBAS — S11-TPE_4

## 1. Requisitos Previos
- Python 3.10 o superior instalado
- Editor: Visual Studio Code
- Conexión a internet (solo para instalación de paquetes)

## 2. Instalación de Dependencias
```bash
# Verificar versión
python --version

# Instalar Flask
pip install flask

# Clonar o descargar archivos del repositorio
cd carpeta_del_proyecto

# EJECUCION DE LA SIMULACION EN ENTORNO CONTROLADO
# Paso 1 - INICIAR EL SERVIDOR
Ejecutar en terminal nueva python app_vulnerable.py
Mensaje esperado: Servidor vulnerable en http://127.0.0.1:5000

#Paso 2 - ACCESO NORMAL
•  Abrir navegador en http://127.0.0.1:5000 
•  Usuario: admin | Contraseña: Admin123! → Acceso concedido

# Paso 3 - EJECUTAR EL ATAQUE
Ejecutar en terminal nueva python ataque_sql_i.py
Resultados esperados:
Prueba 1: Acceso normal 
Prueba 2: Bypass → VULNERABILIDAD CONFIRMADA 
Prueba 3: Extracción → Se filtraron datos 

# Paso 4 - PRUEBA DEL SISTEMA PROTEGIDO
Detener servidor anterior (Ctrl+C) e iniciar versión segura
Ejecutar en terminal nueva python app_seguro.py
-Servidor en http://127.0.0.1:5001
-Repetir ataque
Modificar ataque_sql_i.py → DESTINO = "http://127.0.0.1:5001" y ejecutar:
Ejecutar en terminal nueva python ataque_sql_i.py
-Resultados: Todos los ataques quedan bloqueados 

# PASO 5 - ESCANEO DE RED
Ejecutar en terminal nueva python escaneo_red.py
Muestra puertos abiertos en el equipo local. Documentar servicios identificados
