"""
Módulo de lógica para la gestión de productos.
Versión: 0.5
"""

CATEGORIAS = ("Electrónica", "Alimentos", "Hogar", "Otros")

def agregar_producto(inventario, nombre, precio, categoria, en_oferta):
    """Agrega un producto con precio, categoría y estado de oferta."""
    inventario[nombre] = {
        "precio": precio, 
        "categoria": categoria,
        "oferta": en_oferta  # Nuevo campo booleano
    }
    return inventario

def eliminar_producto(inventario, nombre):
    """Elimina un producto del diccionario si existe."""
    if nombre in inventario:
        del inventario[nombre]
        return True, inventario
    return False, inventario

def obtener_lista_inventario(inventario):
    """Retorna el inventario formateado, resaltando las ofertas."""
    if not inventario:
        return "El inventario está vacío."
    
    lineas = []
    for prod, info in inventario.items():
        # Lógica para mostrar etiqueta de oferta
        etiqueta_oferta = " (EN OFERTA)" if info['oferta'] else ""
        lineas.append(f"- {prod}{etiqueta_oferta} [{info['categoria']}]: ${info['precio']:.2f}")
    return "\n".join(lineas)