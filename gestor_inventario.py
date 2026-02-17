"""
Módulo de lógica para la gestión de productos.
Versión: 0.8 - Estable
"""
import re
import csv

# Lista global de categorías (permitimos que crezca dinámicamente)
CATEGORIAS = ["Electrónica", "Alimentos", "Hogar", "Otros"]

def validar_nombre(nombre):
    """Failsafe: Permite solo letras, números y espacios."""
    if not re.match("^[a-zA-Z0-9 ]*$", nombre):
        return False
    return len(nombre.strip()) > 0

def agregar_producto(inventario, nombre, precio, categoria, en_oferta):
    """Genera un ID único y guarda el producto en el diccionario."""
    if not inventario:
        nuevo_id = "1"
    else:
        # Buscamos el número más alto y sumamos 1 para el nuevo ID
        nuevo_id = str(max(int(k) for k in inventario.keys()) + 1)
        
    inventario[nuevo_id] = {
        "nombre": nombre,
        "precio": precio, 
        "categoria": categoria,
        "oferta": en_oferta
    }
    return inventario, nuevo_id

def eliminar_por_codigo(inventario, codigo):
    """Elimina por ID y retorna el nombre del producto borrado para informar."""
    if codigo in inventario:
        nombre = inventario[codigo]["nombre"]
        del inventario[codigo]
        return True, nombre
    return False, None

def obtener_inventario_por_categoria(inventario, categoria_filtro):
    """Filtra y formatea los productos para mostrar en consola."""
    lineas = []
    for cod, info in inventario.items():
        if info["categoria"] == categoria_filtro:
            tag = " [OFERTA]" if info["oferta"] else ""
            lineas.append(f"ID: {cod} | {info['nombre']}{tag} - ${info['precio']:.2f}")
    
    if not lineas:
        return f"No hay productos registrados en {categoria_filtro}."
    return "\n".join(lineas)

def exportar_a_csv(inventario, nombre_archivo="reporte_inventario.csv"):
    """Crea un archivo compatible con Excel ordenado por categorías."""
    if not inventario:
        return False, "El inventario está vacío. Agregue productos primero."

    try:
        with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
            # Usamos punto y coma para que Excel lo detecte como columnas automáticamente
            escritor = csv.writer(archivo, delimiter=';')
            
            # Encabezados del Excel
            escritor.writerow(['ID', 'Categoría', 'Producto', 'Precio', '¿En Oferta?'])
            
            # Ordenamos los productos por categoría antes de escribir
            productos_ordenados = sorted(
                inventario.items(), 
                key=lambda x: x[1]['categoria']
            )
            
            for cod, info in productos_ordenados:
                oferta_texto = "SÍ" if info['oferta'] else "NO"
                escritor.writerow([
                    cod, 
                    info['categoria'], 
                    info['nombre'], 
                    f"{info['precio']:.2f}", 
                    oferta_texto
                ])
                
        return True, nombre_archivo
    except Exception as e:
        return False, str(e)