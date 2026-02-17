"""
Módulo de lógica para la gestión de productos.
Versión: 0.2
"""

def agregar_producto(inventario, nombre, precio):
    """Agrega o actualiza un producto en el diccionario."""
    inventario[nombre] = precio
    return inventario

def obtener_lista_inventario(inventario):
    """Retorna una lista formateada de los productos."""
    if not inventario:
        return "El inventario está vacío."
    
    lineas = [f"- {prod}: ${prec:.2f}" for prod, prec in inventario.items()]
    return "\n".join(lineas)