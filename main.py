"""
Sistema de Gestión de Inventario Profesional
Versión: 0.8
"""
import gestor_inventario as gestor

def ejecutar_sistema():
    inventario = {} # Estructura principal de datos
    
    while True:
        print(f"\n--- SISTEMA DE GESTIÓN (v0.8) ---")
        print("1. Agregar Producto")
        print("2. Ver Inventario por Categoría")
        print("3. Eliminar Producto por Código")
        print("4. Administrar Categorías")
        print("5. Exportar Reporte para Excel")
        print("6. Salir")
        
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            nombre = input("Nombre del producto: ").strip()
            if not gestor.validar_nombre(nombre):
                print("¡ERROR: Nombre inválido (no use símbolos)! ")
                continue

            print("\nCategorías disponibles:")
            for i, c in enumerate(gestor.CATEGORIAS, 1):
                print(f"{i}. {c}")
            
            try:
                idx = int(input("Seleccione el número de categoría: ")) - 1
                cat = gestor.CATEGORIAS[idx]
                
                print("¿El producto está en oferta?")
                print("1. Sí / 2. No")
                es_oferta = input("Seleccione: ") == "1"

                precio = float(input(f"Ingrese precio para '{nombre}': "))
                if precio <= 0:
                    print("¡ERROR: El precio debe ser mayor a cero!")
                    continue

                inventario, nuevo_id = gestor.agregar_producto(
                    inventario, nombre, precio, cat, es_oferta
                )
                print(f"\n¡ÉXITO: Producto '{nombre}' registrado con ID: {nuevo_id}!")

            except (ValueError, IndexError):
                print("¡ERROR: Selección de categoría o precio inválido!")

        elif opcion == "2":
            print("\n¿Qué categoría desea visualizar?")
            for i, c in enumerate(gestor.CATEGORIAS, 1):
                print(f"{i}. {c}")
            try:
                idx = int(input("Número: ")) - 1
                cat = gestor.CATEGORIAS[idx]
                print(f"\n--- LISTADO DE {cat.upper()} ---")
                print(gestor.obtener_inventario_por_categoria(inventario, cat))
            except:
                print("¡ERROR: Selección inválida!")

        elif opcion == "3":
            cod = input("Ingrese el CÓDIGO (ID) del producto a eliminar: ")
            exito, nombre_borrado = gestor.eliminar_por_codigo(inventario, cod)
            if exito:
                print(f"¡ÉXITO: El producto '{nombre_borrado}' ha sido eliminado!")
            else:
                print("¡ERROR: El código no existe!")

        elif opcion == "4":
            print("\n--- ADMINISTRAR CATEGORÍAS ---")
            print(f"Actuales: {gestor.CATEGORIAS}")
            nueva_cat = input("Nombre de la nueva categoría: ").capitalize().strip()
            if gestor.validar_nombre(nueva_cat):
                if nueva_cat not in gestor.CATEGORIAS:
                    gestor.CATEGORIAS.append(nueva_cat)
                    print(f"¡Categoría '{nueva_cat}' añadida!")
                else:
                    print("Esa categoría ya existe.")
            else:
                print("Nombre de categoría no permitido.")

        elif opcion == "5":
            exito, mensaje = gestor.exportar_a_csv(inventario)
            if exito:
                print(f"\n¡REPORTE GENERADO! Archivo: {mensaje}")
            else:
                print(f"\n¡ERROR: {mensaje}")

        elif opcion == "6":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente del 1 al 6.")

if __name__ == "__main__":
    ejecutar_sistema()