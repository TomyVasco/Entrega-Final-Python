import sqlite3
import os

# --- Configuración de la Base de Datos ---

# Nombre del archivo de la base de datos
DB_NAME = 'inventario.db'

def crear_conexion():
    """Crea y devuelve un objeto de conexión a la base de datos."""
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

def crear_tabla():
    """Crea la tabla 'productos' si no existe."""
    conn = crear_conexion()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    cantidad INTEGER NOT NULL,
                    precio REAL NOT NULL,
                    categoria TEXT
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la tabla: {e}")
        finally:
            conn.close()

# --- Funcionalidades de la Aplicación ---

def registrar_producto():
    """Permite al usuario registrar un nuevo producto."""
    print("\n--- REGISTRAR NUEVO PRODUCTO ---")
    try:
        nombre = input("Nombre del producto (obligatorio): ").strip()
        if not nombre:
            print("El nombre no puede estar vacío.")
            return

        descripcion = input("Descripción del producto: ").strip()

        # Validación de la cantidad
        cantidad_str = input("Cantidad disponible (obligatorio, entero): ").strip()
        if not cantidad_str.isdigit():
            print("La cantidad debe ser un número entero.")
            return
        cantidad = int(cantidad_str)

        # Validación del precio
        precio_str = input("Precio (obligatorio, real): ").strip()
        try:
            precio = float(precio_str)
            if precio < 0:
                print("El precio no puede ser negativo.")
                return
        except ValueError:
            print("El precio debe ser un número real válido.")
            return

        categoria = input("Categoría del producto: ").strip()

        conn = crear_conexion()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?)",
                    (nombre, descripcion, cantidad, precio, categoria)
                )
                conn.commit()
                print(f"Producto '{nombre}' registrado con éxito. ID: {cursor.lastrowid}")
            except sqlite3.Error as e:
                print(f"Error al registrar el producto: {e}")
            finally:
                conn.close()

    except Exception as e:
        print(f"Ocurrió un error inesperado durante el registro: {e}")

def visualizar_productos():
    """Muestra todos los productos registrados en la base de datos."""
    print("\n--- LISTADO DE PRODUCTOS ---")
    conn = crear_conexion()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, cantidad, precio, categoria FROM productos ORDER BY id ASC")
            productos = cursor.fetchall()

            if not productos:
                print("No hay productos registrados en el inventario.")
                return

            # Formato de cabecera de la tabla
            print("-" * 75)
            print(f"| {'ID': <3} | {'NOMBRE': <25} | {'CANTIDAD': <8} | {'PRECIO': <10} | {'CATEGORÍA': <15} |")
            print("-" * 75)

            # Imprimir filas de productos
            for prod in productos:
                # Formato del precio con dos decimales
                precio_f = f"${prod[3]:.2f}"
                print(f"| {prod[0]: <3} | {prod[1]: <25} | {prod[2]: <8} | {precio_f: <10} | {prod[4]: <15} |")

            print("-" * 75)

        except sqlite3.Error as e:
            print(f"Error al visualizar productos: {e}")
        finally:
            conn.close()

def actualizar_producto():
    """Permite actualizar los datos de un producto existente por su ID."""
    print("\n--- ACTUALIZAR PRODUCTO ---")
    id_producto = input("Introduce el ID del producto a actualizar: ").strip()
    if not id_producto.isdigit():
        print("El ID debe ser un número entero.")
        return

    id_producto = int(id_producto)
    conn = crear_conexion()
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Verificar si el producto existe y obtener sus datos actuales
            cursor.execute("SELECT nombre, descripcion, cantidad, precio, categoria FROM productos WHERE id = ?", (id_producto,))
            producto_actual = cursor.fetchone()

            if not producto_actual:
                print(f"Producto con ID {id_producto} no encontrado.")
                return

            print("\nDatos actuales:", producto_actual)
            print("Introduce nuevos valores (deja vacío para mantener el valor actual):")

            # Solicitar nuevos datos. Si se deja vacío, se usa el valor actual.
            nombre = input(f"Nuevo nombre ({producto_actual[0]}): ").strip() or producto_actual[0]
            descripcion = input(f"Nueva descripción ({producto_actual[1] or 'Vacío'}): ").strip() or producto_actual[1]
            categoria = input(f"Nueva categoría ({producto_actual[4] or 'Vacío'}): ").strip() or producto_actual[4]

            # Manejo de cantidad
            cantidad_str = input(f"Nueva cantidad ({producto_actual[2]}): ").strip()
            if cantidad_str:
                if not cantidad_str.isdigit():
                    print("La cantidad debe ser un número entero. Actualización cancelada.")
                    return
                cantidad = int(cantidad_str)
            else:
                cantidad = producto_actual[2]

            # Manejo de precio
            precio_str = input(f"Nuevo precio ({producto_actual[3]:.2f}): ").strip()
            if precio_str:
                try:
                    precio = float(precio_str)
                    if precio < 0:
                        print("El precio no puede ser negativo. Actualización cancelada.")
                        return
                except ValueError:
                    print("El precio debe ser un número real válido. Actualización cancelada.")
                    return
            else:
                precio = producto_actual[3]


            # Ejecutar la actualización
            cursor.execute(
                "UPDATE productos SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ? WHERE id = ?",
                (nombre, descripcion, cantidad, precio, categoria, id_producto)
            )
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Producto con ID {id_producto} actualizado con éxito.")
            else:
                print(f"Producto con ID {id_producto} no encontrado (o no se realizaron cambios).")

        except sqlite3.Error as e:
            print(f"Error al actualizar el producto: {e}")
        finally:
            conn.close()

def eliminar_producto():
    """Permite eliminar un producto por su ID."""
    print("\n--- ELIMINAR PRODUCTO ---")
    id_producto = input("Introduce el ID del producto a eliminar: ").strip()
    if not id_producto.isdigit():
        print("El ID debe ser un número entero.")
        return

    id_producto = int(id_producto)
    conn = crear_conexion()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
            conn.commit()

            if cursor.rowcount > 0:
                print(f"Producto con ID {id_producto} eliminado con éxito.")
            else:
                print(f"Producto con ID {id_producto} no encontrado.")

        except sqlite3.Error as e:
            print(f"Error al eliminar el producto: {e}")
        finally:
            conn.close()

def buscar_productos():
    """Busca productos por ID, Nombre o Categoría."""
    print("\n--- BÚSQUEDA DE PRODUCTOS ---")
    print("Buscar por:")
    print("1. ID")
    print("2. Nombre")
    print("3. Categoría")
    opcion = input("Introduce tu opción (1/2/3): ").strip()

    conn = crear_conexion()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        query = None
        param = None

        if opcion == '1':
            id_producto = input("Introduce el ID: ").strip()
            if id_producto.isdigit():
                query = "SELECT * FROM productos WHERE id = ?"
                param = (int(id_producto),)
            else:
                print("ID inválido.")
                return
        elif opcion == '2':
            nombre = input("Introduce el Nombre (o parte del nombre): ").strip()
            query = "SELECT * FROM productos WHERE nombre LIKE ?"
            param = (f"%{nombre}%",)
        elif opcion == '3':
            categoria = input("Introduce la Categoría: ").strip()
            query = "SELECT * FROM productos WHERE categoria LIKE ?"
            param = (f"%{categoria}%",)
        else:
            print("Opción no válida.")
            return

        cursor.execute(query, param)
        resultados = cursor.fetchall()

        if not resultados:
            print("No se encontraron productos con ese criterio.")
            return

        # Imprimir resultados (cabecera con todos los campos)
        print("-" * 120)
        print(f"| {'ID': <3} | {'NOMBRE': <20} | {'DESCRIPCIÓN': <40} | {'CANTIDAD': <8} | {'PRECIO': <10} | {'CATEGORÍA': <15} |")
        print("-" * 120)

        for prod in resultados:
            precio_f = f"${prod[4]:.2f}"
            print(f"| {prod[0]: <3} | {prod[1]: <20} | {prod[2]: <40} | {prod[3]: <8} | {precio_f: <10} | {prod[5]: <15} |")

        print("-" * 120)

    except sqlite3.Error as e:
        print(f"Error al buscar productos: {e}")
    finally:
        conn.close()

def generar_reporte_stock_bajo():
    """Genera un reporte de productos con cantidad igual o inferior a un límite."""
    print("\n--- REPORTE DE STOCK BAJO ---")
    limite_str = input("Introduce el límite de cantidad (Stock Bajo si <= este número): ").strip()

    if not limite_str.isdigit():
        print("El límite debe ser un número entero.")
        return

    limite = int(limite_str)
    conn = crear_conexion()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nombre, cantidad, precio, categoria FROM productos WHERE cantidad <= ? ORDER BY cantidad ASC",
                (limite,)
            )
            productos = cursor.fetchall()

            print(f"\n--- Productos con Cantidad <= {limite} ---")
            if not productos:
                print("Todos los productos tienen una cantidad superior al límite especificado.")
                return

            # Formato de cabecera de la tabla
            print("-" * 75)
            print(f"| {'ID': <3} | {'NOMBRE': <25} | {'CANTIDAD': <8} | {'PRECIO': <10} | {'CATEGORÍA': <15} |")
            print("-" * 75)

            # Imprimir filas de productos
            for prod in productos:
                precio_f = f"${prod[3]:.2f}"
                print(f"| {prod[0]: <3} | {prod[1]: <25} | {prod[2]: <8} | {precio_f: <10} | {prod[4]: <15} |")

            print("-" * 75)

        except sqlite3.Error as e:
            print(f"Error al generar el reporte: {e}")
        finally:
            conn.close()

# --- Interfaz de Usuario (Menú Principal) ---

def mostrar_menu():
    """Muestra el menú principal de la aplicación."""
    os.system('cls' if os.name == 'nt' else 'clear') # Limpia la consola
    print("=========================================")
    print("   SISTEMA DE GESTIÓN DE INVENTARIO      ")
    print("=========================================")
    print("1. Registrar nuevo producto")
    print("2. Visualizar todos los productos")
    print("3. Actualizar producto por ID")
    print("4. Eliminar producto por ID")
    print("5. Buscar productos (ID/Nombre/Categoría)")
    print("6. Reporte de Stock Bajo")
    print("7. Salir")
    print("-----------------------------------------")
    opcion = input("Elige una opción: ").strip()
    return opcion

def main():
    """Función principal que ejecuta la lógica de la aplicación."""
    crear_tabla() # Asegura que la tabla exista al iniciar

    while True:
        opcion = mostrar_menu()

        if opcion == '1':
            registrar_producto()
        elif opcion == '2':
            visualizar_productos()
        elif opcion == '3':
            actualizar_producto()
        elif opcion == '4':
            eliminar_producto()
        elif opcion == '5':
            buscar_productos()
        elif opcion == '6':
            generar_reporte_stock_bajo()
        elif opcion == '7':
            print("\nSaliendo del sistema de inventario. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

        # Esperar la pulsación de una tecla antes de volver al menú
        if opcion in ['1', '2', '3', '4', '5', '6']:
            input("\nPresiona ENTER para volver al menú principal...")

# Ejecución del programa
if __name__ == "__main__":
    main()