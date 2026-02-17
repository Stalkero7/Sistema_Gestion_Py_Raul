import gestor_inventario as gestor

VERSION = "0.7"

def ejecutar_sistema():
    inventario = {}
    
    while True:
        print(f"\n--- SISTEMA DE GESTIÓN (v{VERSION}) ---")
        print("1. Agregar Producto\n2. Ver por Categoría\n3. Eliminar por Código\n4. Agregar Nueva Categoría\n5. Salir")
        opcion = input("Seleccione: ")

        if opcion == "1":
            nombre = input("Nombre del producto: ").strip()
            
            # Failsafe 1: Validación de nombre (símbolos)
            if not gestor.validar_nombre(nombre):
                print("¡ERROR: El nombre contiene símbolos inválidos o está vacío!")
                continue

            print("Categorías:")
            for i, c in enumerate(gestor.CATEGORIAS, 1):
                print(f"{i}. {c}")
            
            try:
                idx = int(input("Seleccione número de categoría: ")) - 1
                cat = gestor.CATEGORIAS[idx]
                
                # Failsafe 2: Validación de oferta
                oferta_in = input("¿En oferta? (1: Sí / 2: No): ")
                if oferta_in not in ["1", "2"]:
                    print("¡ERROR: Opción de oferta inválida!")
                    continue
                es_oferta = oferta_in == "1"

                # Failsafe 3: Validación de precio (tipo de dato)
                precio_raw = input("Ingrese el precio: ")
                precio = float(precio_raw)
                
                if precio <= 0:
                    print("¡ERROR: El precio debe ser mayor a 0!")
                    continue

                inventario, nuevo_id = gestor.agregar_producto(inventario, nombre, precio, cat, es_oferta)
                print(f"¡ÉXITO: '{nombre}' registrado con ID: {nuevo_id}!")

            except ValueError:
                print("¡ERROR: Precio inválido. Use solo números (ej: 1500.50)!")
            except IndexError:
                print("¡ERROR: El número de categoría no existe!")

        elif opcion == "2":
            # (Lógica de filtrado con failsafe de índice)
            try:
                for i, c in enumerate(gestor.CATEGORIAS, 1): print(f"{i}. {c}")
                idx = int(input("Número: ")) - 1
                cat = gestor.CATEGORIAS[idx]
                print(f"\n--- {cat.upper()} ---")
                print(gestor.obtener_inventario_por_categoria(inventario, cat))
            except (ValueError, IndexError):
                print("¡ERROR: Selección de categoría inválida!")

        elif opcion == "3":
            cod = input("Ingrese el CÓDIGO (ID) a eliminar: ")
            exito, nombre = gestor.eliminar_por_codigo(inventario, cod)
            if exito:
                print(f"¡ÉXITO: {nombre} (ID: {cod}) eliminado!")
            else:
                print("¡ERROR: El código no existe en el sistema!")

        elif opcion == "4":
            nueva_cat = input("Nombre de la nueva categoría: ").capitalize().strip()
            if gestor.validar_nombre(nueva_cat):
                if nueva_cat not in gestor.CATEGORIAS:
                    gestor.CATEGORIAS.append(nueva_cat)
                    print(f"¡ÉXITO: Categoría '{nueva_cat}' añadida!")
                else:
                    print("¡AVISO: Esa categoría ya existe!")
            else:
                print("¡ERROR: Nombre de categoría inválido!")

        elif opcion == "5":
            print("Cerrando sistema de forma segura...")
            break

if __name__ == "__main__":
    ejecutar_sistema()