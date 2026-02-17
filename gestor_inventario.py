"""
Módulo de lógica para la gestión de productos.
Versión: 0.9 - Con Persistencia de Datos (JSON)
"""
import re
import csv
import json # Nueva librería para la persistencia de datos
import os   # Para verificar si el archivo existe antes de cargarlo

CATEGORIAS = ["Electrónica", "Alimentos", "Hogar", "Otros"]
ARCHIVO_DATOS = "inventario.json"

def guardar_datos(inventario):
    """Guarda el inventario y las categorías en un archivo JSON."""
    datos = {
        "inventario": inventario,
        "categorias": CATEGORIAS
    }
    try:
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)
        return True
    except Exception as e:
        print(f"Error al guardar: {e}")
        return False

def cargar_datos():
    """Carga el inventario y las categorías desde el archivo JSON."""
    global CATEGORIAS
    if os.path.exists(ARCHIVO_DATOS):
        try:
            with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                datos = json.load(f)
                CATEGORIAS = datos.get("categorias", CATEGORIAS)
                return datos.get("inventario", {})
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            return {}
    return {}

def validar_nombre(nombre):
    """Failsafe: Permite solo letras, números y espacios."""
    if not re.match("^[a-zA-Z0-9 ]*$", nombre):
        return False
    return len(nombre.strip()) > 0

def agregar_producto(inventario, nombre, precio, categoria, en_oferta):
    """Genera un ID único y guarda el producto."""
    if not inventario:
        nuevo_id = "1"
    else:
        nuevo_id = str(max(int(k) for k in inventario.keys()) + 1)
        
    inventario[nuevo_id] = {
        "nombre": nombre,
        "precio": precio, 
        "categoria": categoria,
        "oferta": en_oferta
    }
    guardar_datos(inventario) # Guardado automático
    return inventario, nuevo_id

def eliminar_por_codigo(inventario, codigo):
    """Elimina por ID y actualiza el archivo."""
    if codigo in inventario:
        nombre = inventario[codigo]["nombre"]
        del inventario[codigo]
        guardar_datos(inventario) # Guardado automático
        return True, nombre
    return False, None

def obtener_inventario_por_categoria(inventario, categoria_filtro):
    lineas = []
    for cod, info in inventario.items():
        if info["categoria"] == categoria_filtro:
            tag = " [OFERTA]" if info["oferta"] else ""
            lineas.append(f"ID: {cod} | {info['nombre']}{tag} - ${info['precio']:.2f}")
    
    if not lineas:
        return f"No hay productos registrados en {categoria_filtro}."
    return "\n".join(lineas)

def exportar_a_csv(inventario, nombre_archivo="reporte_inventario.csv"):
    if not inventario:
        return False, "El inventario está vacío."
    try:
        with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo, delimiter=';')
            escritor.writerow(['ID', 'Categoría', 'Producto', 'Precio', '¿En Oferta?'])
            productos_ordenados = sorted(inventario.items(), key=lambda x: x[1]['categoria'])
            for cod, info in productos_ordenados:
                oferta_texto = "SÍ" if info['oferta'] else "NO"
                escritor.writerow([cod, info['categoria'], info['nombre'], f"{info['precio']:.2f}", oferta_texto])
        return True, nombre_archivo
    except Exception as e:
        return False, str(e)