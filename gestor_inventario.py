"""
Módulo de lógica para la gestión de productos.
Versión: 1.1 - Estable
"""
import json
import os
import re
import csv

# Lista de categorías que persiste en el JSON
CATEGORIAS = ["Electrónica", "Alimentos", "Hogar", "Otros"]
ARCHIVO_DATOS = "inventario.json"

def validar_nombre(nombre):
    """Valida que el nombre sea alfanumérico y no esté vacío."""
    if not nombre or not re.match("^[a-zA-Z0-9 ]*$", nombre):
        return False
    # Enforce a sensible maximum length to avoid excessively long names
    if len(nombre.strip()) > 100:
        return False
    return len(nombre.strip()) > 0

def cargar_datos():
    """Carga inventario y categorías desde JSON."""
    global CATEGORIAS
    if not os.path.exists(ARCHIVO_DATOS):
        return {}
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            datos = json.load(f)
            CATEGORIAS = datos.get("categorias", CATEGORIAS)
            return datos.get("inventario", {})
    except:
        return {}

def guardar_datos(inventario):
    """Guarda el estado actual del sistema (Productos y Categorías)."""
    try:
        datos = {"inventario": inventario, "categorias": CATEGORIAS}
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error al guardar: {e}")

def agregar_producto(inventario, nombre, precio, categoria, en_oferta):
    """Genera ID y registra el producto."""
    # Generación de ID basada en el máximo actual
    ids_numericos = [int(k) for k in inventario.keys()]
    nuevo_id = str(max(ids_numericos + [0]) + 1)
    
    inventario[nuevo_id] = {
        "nombre": nombre,
        "precio": precio,
        "categoria": categoria,
        "oferta": en_oferta
    }
    guardar_datos(inventario)
    return inventario, nuevo_id

def obtener_listado_por_categoria(inventario, categoria_filtro):
    """Retorna una lista de strings con ID y Nombre de productos filtrados."""
    resultados = []
    for id_prod, info in inventario.items():
        if info["categoria"] == categoria_filtro:
            oferta_tag = " [OFERTA]" if info["oferta"] else ""
            resultados.append(f"ID: {id_prod} | {info['nombre']}{oferta_tag} - ${info['precio']:.2f}")
    return resultados

def eliminar_por_id(inventario, id_prod):
    """Elimina producto y actualiza archivo."""
    if id_prod in inventario:
        nombre = inventario[id_prod]["nombre"]
        del inventario[id_prod]
        guardar_datos(inventario)
        return True, nombre
    return False, None

def exportar_csv(inventario):
    """Crea el archivo Excel/CSV con delimitador de punto y coma."""
    if not inventario:
        return False, "Inventario vacío"
    nombre_archivo = "reporte_inventario.csv"
    try:
        with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f, delimiter=';')
            escritor.writerow(['ID', 'CATEGORIA', 'PRODUCTO', 'PRECIO', 'OFERTA'])
            for k, v in inventario.items():
                oferta = "SI" if v['oferta'] else "NO"
                escritor.writerow([k, v['categoria'], v['nombre'], v['precio'], oferta])
        return True, nombre_archivo
    except:
        return False, "Error de escritura en disco"