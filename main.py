"""
Sistema de Gestión de Inventario Profesional
Versión: 0.9 - Con Persistencia
"""
import gestor_inventario as gestor

def ejecutar_sistema():
    # REQUERIMIENTO: Carga de datos al iniciar
    inventario = gestor.cargar_datos()
    
    while True:
        print(f"\n--- SISTEMA DE GESTIÓN (v0.9) ---")
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
                print("¡ERROR: Nombre inválido!")
                continue

            print("\nCategorías:")
            for i, c in enumerate(gestor.gestor_inventario.CATEGORIAS if hasattr(gestor, 'gestor_inventario') else gestor.CATEGORIAS, 1):
                print(f"{i}. {c}")
            
            try:
                idx = int(input("Número de categoría: ")) - 1
                cat = gestor.CATEGORIAS[idx]
                es_oferta = input("¿En oferta? (1: Sí / 2: No): ") == "1"
                precio = float(input(f"Precio: "))
                
                if precio <= 0:
                    print("¡ERROR: Precio debe ser mayor a 0!")
                    continue

                inventario, nuevo_id = gestor.agregar_producto(inventario, nombre, precio, cat, es_oferta)
                print(f"¡ÉXITO: Registrado con ID: {nuevo_id}!")
            except (ValueError, IndexError):
                print("¡ERROR: Entrada inválida!")

        elif opcion == "2":
            for i, c in enumerate(gestor.CATEGORIAS, 1): print(f"{i}. {c}")
            try:
                idx = int(input("Número: ")) - 1
                cat = gestor.CATEGORIAS[idx]
                print(f"\n--- LISTADO DE {cat.upper()} ---")
                print(gestor.obtener_inventario_por_categoria(inventario, cat))
            except:
                print("¡ERROR: Selección inválida!")

        elif opcion == "3":
            cod = input("Ingrese el ID a eliminar: ")
            exito, nombre_borrado = gestor.eliminar_por_codigo(inventario, cod)
            if exito:
                print(f"¡ÉXITO: '{nombre_borrado}' eliminado!")
            else:
                print("¡ERROR: ID no encontrado!")

        elif opcion == "4":
            nueva_cat = input("Nueva categoría: ").capitalize().strip()
            if gestor.validar_nombre(nueva_cat) and nueva_cat not in gestor.CATEGORIAS:
                gestor.CATEGORIAS.append(nueva_cat)
                gestor.guardar_datos(inventario) # Guardamos la nueva lista de categorías
                print(f"¡Categoría '{nueva_cat}' añadida!")
            else:
                print("¡ERROR: Nombre inválido o ya existe!")

        elif opcion == "5":
            exito, mensaje = gestor.exportar_a_csv(inventario)
            print(f"¡REPORTE GENERADO! {mensaje}" if exito else f"Error: {mensaje}")

        elif opcion == "6":
            # Guardamos una última vez antes de salir por seguridad
            gestor.guardar_datos(inventario)
            print("Datos guardados. Cerrando sistema...")
            break

if __name__ == "__main__":
    ejecutar_sistema()