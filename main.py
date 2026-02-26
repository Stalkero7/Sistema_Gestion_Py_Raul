"""
Ejecutable Principal: Interfaz de Consola
Versión: 1.1
"""
import gestor_inventario as gestor

def safe_input(prompt, max_len=100):
    """Read input and enforce a maximum length (re-prompt if exceeded)."""
    while True:
        s = input(prompt)
        if len(s) <= max_len:
            return s
        print(f"Entrada demasiado larga (máx {max_len} caracteres). Intente de nuevo.")


def ejecutar_sistema():
    # Carga de datos persistentes al iniciar el programa
    inventario = gestor.cargar_datos()
    
    while True:
        print(f"\n================================")
        print(f"   SISTEMA DE GESTIÓN (v1.1)")
        print(f"================================")
        print("1. Registrar Producto")
        print("2. Ver Productos por Categoría")
        print("3. Eliminar por ID")
        print("4. Administrar Categorías")
        print("5. Exportar a Excel (CSV)")
        print("6. Modificar Precio")
        print("7. Salir")
        
        opc = safe_input("\nSeleccione una opción: ").strip()

        if opc == "1":
            # --- REGISTRO CON FAILSAFES Y OPCIÓN DE CANCELAR ---
            nombre = safe_input("\nNombre del producto (0 para cancelar): ").strip()
            if nombre == "0": continue
            if not gestor.validar_nombre(nombre):
                print("¡ERROR: Nombre inválido o vacío!"); continue
            
            print("\nSeleccione Categoría (0 para cancelar):")
            for i, c in enumerate(gestor.CATEGORIAS, 1): print(f"{i}. {c}")
            
            cat_input = safe_input("Número: ").strip()
            if cat_input == "0": continue
            try:
                cat = gestor.CATEGORIAS[int(cat_input) - 1]
            except (ValueError, IndexError):
                print("¡ERROR: Opción de categoría no válida!"); continue

            oferta_input = safe_input("¿Está en oferta? (1: Sí / 2: No / 0: Cancelar): ").strip()
            if oferta_input == "0": continue
            oferta = oferta_input == "1"

            try:
                precio_in = safe_input("Precio (0 para cancelar): ").strip()
                if precio_in == "0": continue
                precio = float(precio_in)
                if precio <= 0:
                    print("¡PRECIO INVÁLIDO: Debe ser mayor a 0!"); continue
                print("¡Precio registrado!")
            except ValueError:
                print("¡ERROR: El precio debe ser un número!"); continue

            inventario, nuevo_id = gestor.agregar_producto(inventario, nombre, precio, cat, oferta)
            print(f"¡ÉXITO: Producto registrado con ID: {nuevo_id}!")

        elif opc == "2":
            # --- VISUALIZACIÓN POR CATEGORÍA CON IDS ---
            print("\n¿Qué categoría desea inspeccionar? (0 para cancelar)")
            for i, c in enumerate(gestor.CATEGORIAS, 1): print(f"{i}. {c}")
            
            ent = safe_input("Número: ").strip()
            if ent == "0": continue
            try:
                idx = int(ent) - 1
                cat = gestor.CATEGORIAS[idx]
                print(f"\n--- PRODUCTOS EN {cat.upper()} ---")
                productos = gestor.obtener_listado_por_categoria(inventario, cat)
                if productos:
                    for p in productos: print(p)
                else:
                    print("No hay productos registrados en esta categoría.")
            except (ValueError, IndexError):
                print("¡OPCIÓN INVÁLIDA: Categoría no existe!")

        elif opc == "3":
            idx = safe_input("\nIngrese el ID a eliminar (0 para cancelar): ").strip()
            if idx == "0": continue
            exito, nombre_del = gestor.eliminar_por_id(inventario, idx)
            if exito:
                print(f"¡ÉXITO: El producto '{nombre_del}' ha sido eliminado!")
            else:
                print("¡ERROR: El ID no existe!"); continue

        elif opc == "4":
            nueva = safe_input("\nNombre de nueva categoría (0 para cancelar): ").capitalize().strip()
            if nueva == "0": continue
            if gestor.validar_nombre(nueva) and nueva not in gestor.CATEGORIAS:
                gestor.CATEGORIAS.append(nueva)
                gestor.guardar_datos(inventario)
                print(f"¡Aprobado: Categoría '{nueva}' añadida!")
            else:
                print("¡ERROR: Nombre no válido o ya existe!")

        elif opc == "5":
            exito, archivo = gestor.exportar_csv(inventario)
            if exito:
                print(f"¡REPORTE GENERADO: {archivo}!")
            else:
                print(f"¡ERROR: {archivo}")

        elif opc == "6":
            idx = safe_input("\nID del producto a modificar (0 para cancelar): ").strip()
            if idx == "0": continue
            if idx in inventario:
                try:
                    nuevo_p_str = safe_input(f"Nuevo precio para {inventario[idx]['nombre']}: ")
                    nuevo_p = float(nuevo_p_str)
                    if nuevo_p > 0:
                        inventario[idx]["precio"] = nuevo_p
                        gestor.guardar_datos(inventario)
                        print("¡PRECIO ACTUALIZADO CON ÉXITO!")
                    else: print("¡ERROR: El precio debe ser mayor a 0!")
                except ValueError: print("¡ERROR: Ingrese un valor numérico!")
            else:
                print("¡ERROR: ID no encontrado!")

        elif opc == "7":
            print("Cerrando sistema de forma segura..."); break
        
        else:
            # MENSAJE PARA OPCIONES FUERA DEL RANGO 1-7
            print("¡OPCIÓN NO VÁLIDA: Por favor seleccione un número del 1 al 7!")

if __name__ == "__main__":
    ejecutar_sistema()