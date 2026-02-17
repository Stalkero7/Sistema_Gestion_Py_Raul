"""
Módulo de lógica para la gestión de productos.
Versión: 0.7
"""

import re # Importamos expresiones regulares para el failsafe de símbolos

CATEGORIAS = ["Electrónica", "Alimentos", "Hogar", "Otros"]

def validar_nombre(nombre):
    """
    Failsafe: Verifica que el nombre no contenga símbolos extraños.
    Permite letras, números y espacios.
    """
    # Usamos regex para permitir solo caracteres alfanuméricos y espacios
    if not re.match("^[a-zA-Z0-9 ]*$", nombre):
        return False
    return len(nombre) > 0

def agregar_producto(inventario, nombre, precio, categoria, en_oferta):
    # Generamos ID basado en el máximo actual para evitar colisiones si se borran
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
    return inventario, nuevo_id

def eliminar_por_codigo(inventario, codigo):
    if codigo in inventario:
        nombre = inventario[codigo]["nombre"]
        del inventario[codigo]
        return True, nombre
    return False, None

def obtener_inventario_por_categoria(inventario, categoria_filtro):
    lineas = []
    for cod, info in inventario.items():
        if info["categoria"] == categoria_filtro:
            tag = " [OFERTA]" if info["oferta"] else ""
            lineas.append(f"ID: {cod} | {info['nombre']}{tag} - ${info['precio']:.2f}")
    return "\n".join(lineas) if lineas else "No hay productos en esta categoría."