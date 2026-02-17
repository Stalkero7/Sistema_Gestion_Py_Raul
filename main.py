import gestor_inventario as gestor

VERSION = "0.5"

def ejecutar_sistema():
    inventario = {}
    
    while True:
        print(f"\n--- SISTEMA DE GESTIÓN (v{VERSION}) ---")
        print("1. Agregar producto\n2. Ver inventario\n3. Eliminar producto\n4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre del producto: ").strip()
            
            # Selección de Categoría
            for i, cat in enumerate(gestor.CATEGORIAS, 1):
                print(f"{i}. {cat}")
            
            try:
                idx_cat = int(input("Número de categoría: "))
                cat_elegida = gestor.CATEGORIAS[idx_cat - 1]
                
                # Preguntar por oferta (Numérico: 1 para Sí, 2 para No)
                print("¿Está en oferta?\n1. Sí\n2. No")
                oferta_opc = input("Seleccione: ")
                es_oferta = True if oferta_opc == "1" else False
                
                precio = float(input(f"Precio para {nombre}: "))
                inventario = gestor.agregar_producto(inventario, nombre, precio, cat_elegida, es_oferta)
                print(f"¡{nombre} guardado!")
                
            except (ValueError, IndexError):
                print("Error: Selección inválida.")

        elif opcion == "2":
            print("\n" + gestor.obtener_lista_inventario(inventario))

        elif opcion == "3":
            nombre_borrar = input("Nombre del producto a eliminar: ").strip()
            exito, inventario = gestor.eliminar_producto(inventario, nombre_borrar)
            if exito:
                print(f"¡{nombre_borrar} eliminado correctamente!")
            else:
                print("Producto no encontrado.")

        elif opcion == "4":
            break

if __name__ == "__main__":
    ejecutar_sistema()