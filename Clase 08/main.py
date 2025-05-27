# Lista principal onde os produtos serão armazenados
productos = []

def agregar_producto():
    nombre = input("Ingrese el nombre del producto: ").strip()
    while not nombre:
        nombre = input("El nombre no puede estar vacío. Intente nuevamente: ").strip()

    categoria = input("Ingrese la categoría del producto: ").strip()
    while not categoria:
        categoria = input("La categoría no puede estar vacía. Intente nuevamente: ").strip()

    while True:
        precio = input("Ingrese el precio del producto (sin centavos): ").strip()
        if precio.isdigit():
            precio = int(precio)
            break
        else:
            print("Debe ingresar un número válido.")

    productos.append([nombre, categoria, precio])
    print("Producto agregado exitosamente.\n")

def mostrar_productos():
    if not productos:
        print("No hay productos registrados.\n")
        return
    print("Lista de productos:")
    for i, producto in enumerate(productos, 1):
        print(f"{i}. Nombre: {producto[0]}, Categoría: {producto[1]}, Precio: ${producto[2]}")
    print()

def buscar_producto():
    termino = input("Ingrese el nombre del producto a buscar: ").strip().lower()
    encontrados = [p for p in productos if termino in p[0].lower()]
    if encontrados:
        print("Productos encontrados:")
        for p in encontrados:
            print(f"Nombre: {p[0]}, Categoría: {p[1]}, Precio: ${p[2]}")
    else:
        print("No se encontraron productos con ese nombre.")
    print()

def eliminar_producto():
    mostrar_productos()
    if not productos:
        return
    while True:
        pos = input("Ingrese el número del producto a eliminar: ").strip()
        if pos.isdigit() and 1 <= int(pos) <= len(productos):
            eliminado = productos.pop(int(pos)-1)
            print(f"Producto '{eliminado[0]}' eliminado exitosamente.\n")
            break
        else:
            print("Número inválido. Intente nuevamente.")

def menu():
    while True:
        print("Sistema de Gestión Básica De Productos")
        print("1. Agregar producto")
        print("2. Mostrar productos")
        print("3. Buscar producto")
        print("4. Eliminar producto")
        print("5. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            agregar_producto()
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            buscar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            print("Gracias por usar el sistema.")
            break
        else:
            print("Opción inválida. Intente nuevamente.\n")

# Iniciar el programa
menu()