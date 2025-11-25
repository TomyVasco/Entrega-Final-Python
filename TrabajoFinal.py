import sqlite3

# Conexión y creación de la tabla
def crear_base():
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
        )
    """)

    conn.commit()
    conn.close()


# Registrar producto
def registrar_producto():
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()

    nombre = input("Nombre del producto: ")
    descripcion = input("Descripción: ")
    cantidad = int(input("Cantidad: "))
    precio = float(input("Precio: "))
    categoria = input("Categoría: ")

    cursor.execute("""
        INSERT INTO productos(nombre, descripcion, cantidad, precio, categoria)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, descripcion, cantidad, precio, categoria))

    conn.commit()
    conn.close()

    print("\nProducto registrado correctamente.\n")


# Mostrar productos
def mostrar_productos():
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    if not productos:
        print("\nNo hay productos registrados.\n")
    else:
        print("\n--- Lista de productos ---")
        for prod in productos:
            print(f"ID: {prod[0]} | Nombre: {prod[1]} | Cantidad: {prod[3]} | Precio: {prod[4]} | Categoría: {prod[5]}")
        print()

    conn.close()


# Buscar producto por ID
def buscar_producto():
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()

    pid = input("ID del producto a buscar: ")

    cursor.execute("SELECT * FROM productos WHERE id = ?", (pid,))
    prod = cursor.fetchone()

    if prod:
        print(f"\nID: {prod[0]}")
        print(f"Nombre: {prod[1]}")
        print(f"Descripción: {prod[2]}")
        print(f"Cantidad: {prod[3]}")
        print(f"Precio: {prod[4]}")
        print(f"Categoría: {prod[5]}\n")
    else:
        print("\nNo se encontró un producto con ese ID.\n")

    conn.close()


# Actualizar producto por ID
def actualizar_producto():
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()

    pid = input("ID del producto a actualizar: ")

    cursor.execute("SELECT * FROM productos WHERE id = ?", (pid,))
    prod = cursor.fetchone()

    if not prod:
        print("\nNo existe un producto con ese ID.\n")
        conn.close()
        return

    nuevo_nombre = input("Nuevo nombre: ")
    nueva_desc = input("Nueva descripción: ")
    nueva_cant = int(input("Nueva cantidad: "))
    nuevo_precio = float(input("Nuevo precio: "))
    nueva_categoria = input("Nueva categoría: ")

    cursor.execute("""
        UPDATE productos 
        SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
        WHERE id = ?
    """, (nuevo_nombre, nueva_desc, nueva_cant, nuevo_precio, nueva_categoria, pid))

    conn.commit()
    conn.close()

    print("\nProducto actualizado correctamente.\n")


# Eliminar producto
def eliminar_producto():
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()

    pid = input("ID del producto a eliminar: ")

    cursor.execute("DELETE FROM productos WHERE id = ?", (pid,))
    conn.commit()
    conn.close()

    print("\nProducto eliminado correctamente (si existía).\n")


# Reporte de productos con cantidad baja
def reporte_bajo_stock():
    limite = int(input("Mostrar productos con cantidad menor o igual a: "))

    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
    productos = cursor.fetchall()

    if not productos:
        print("\nNo hay productos con cantidad igual o inferior al límite.\n")
    else:
        print("\n--- Productos con bajo stock ---")
        for prod in productos:
            print(f"ID: {prod[0]} | Nombre: {prod[1]} | Cantidad: {prod[3]}")
        print()

    conn.close()


# MENÚ PRINCIPAL
def menu():
    crear_base()

    while True:
        print("----- Sistema de Inventario -----")
        print("1. Registrar producto")
        print("2. Mostrar productos")
        print("3. Buscar producto por ID")
        print("4. Actualizar producto")
        print("5. Eliminar producto")
        print("6. Reporte bajo stock")
        print("7. Salir")

        opcion = input("Elegí una opción: ")

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            buscar_producto()
        elif opcion == "4":
            actualizar_producto()
        elif opcion == "5":
            eliminar_producto()
        elif opcion == "6":
            reporte_bajo_stock()
        elif opcion == "7":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida.\n")


menu()