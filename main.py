import gestor_inventario as gestor # Importamos nuestro módulo

VERSION = "0.2"

def mostrar_menu():
    print(f"\n--- SISTEMA DE GESTIÓN (v{VERSION}) ---")
    print("1. Agregar producto")
    print("2. Ver inventario")
    print("3. Salir")

def ejecutar_sistema():
    inventario = {}
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre del producto: ").strip()
            try:
                precio = float(input(f"Precio para {nombre}: "))
                # Usamos la función del módulo modularizado
                inventario = gestor.agregar_producto(inventario, nombre, precio)
                print(f"¡{nombre} actualizado!")
            except ValueError:
                print("Error: Ingrese un número válido.")
        
        elif opcion == "2":
            # Obtenemos la información procesada por el módulo
            print("\nInventario Actual:")
            print(gestor.obtener_lista_inventario(inventario))
        
        elif opcion == "3":
            print("Cerrando sistema...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    ejecutar_sistema()