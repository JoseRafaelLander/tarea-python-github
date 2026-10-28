# Curso: Fundamentos de Tecnología Digitales
# Profesor: Adonis Aleman G.
# Estudiante: Jose Rafael Lander

# modelo.py
# aquí están las listas con los datos y las funciones que las tocan.
# nada de print ni input acá, eso es de la vista y el controlador

import csv

catalogo = []   # productos, cada uno es un diccionario
ventas = []     # ventas que se hacen mientras el programa está abierto
alertas = []    # alertas de stock bajo y de vencimiento


def buscar_producto(codigo):
    # recorre el catálogo y devuelve el producto con ese código
    # si no está devuelve None
    # paso todo a mayúsculas para que "l001" y "L001" sean lo mismo
    codigo = str(codigo).strip().upper()
    for producto in catalogo:
        if producto["codigo"].upper() == codigo:
            return producto
    return None


def existe_codigo(codigo):
    return buscar_producto(codigo) is not None


def agregar_producto(producto):
    # si el código ya existe no lo agrega y devuelve False
    if existe_codigo(producto["codigo"]):
        return False
    # en la etapa 1 poníamos N/A, en esta se deja vacío
    if producto["fecha_vencimiento"].strip().upper() == "N/A":
        producto["fecha_vencimiento"] = ""
    catalogo.append(producto)
    return True


def obtener_productos():
    # mando una copia de la lista para que no la dañen desde afuera
    return list(catalogo)


def aumentar_stock(codigo, cantidad):
    producto = buscar_producto(codigo)
    if producto is None:
        return False
    producto["stock"] = producto["stock"] + cantidad
    return True


def descontar_stock(codigo, cantidad):
    # False si el producto no existe o si no alcanza el stock
    producto = buscar_producto(codigo)
    if producto is None or producto["stock"] < cantidad:
        return False
    producto["stock"] = producto["stock"] - cantidad
    return True


def generar_numero_factura():
    # F-0001, F-0002... según cuántas ventas hay
    return "F-" + str(len(ventas) + 1).zfill(4)


def agregar_venta(venta):
    ventas.append(venta)


def obtener_ventas():
    return list(ventas)


def agregar_alerta(alerta):
    alertas.append(alerta)


def limpiar_alertas():
    # se limpia antes de generar las alertas otra vez, para que no se repitan
    alertas.clear()


def obtener_alertas():
    return list(alertas)


def cargar_datos_desde_csv(ruta):
    # carga los productos del archivo de prueba
    # devuelve cuántos cargó y una lista con los errores que hubo
    cargados = 0
    errores = []
    try:
        with open(ruta, newline="", encoding="utf-8-sig") as archivo:
            lector = csv.DictReader(archivo)
            numero_fila = 1
            for fila in lector:
                numero_fila += 1
                try:
                    producto = {
                        "codigo": fila["codigo"].strip(),
                        "nombre": fila["nombre"].strip(),
                        "categoria": fila["categoria"].strip(),
                        "stock": int(fila["stock"]),
                        "stock_minimo": int(fila["stock_minimo"]),
                        "precio_compra": float(fila["precio_compra"]),
                        "precio_venta": float(fila["precio_venta"]),
                        "fecha_vencimiento": fila["fecha_vencimiento"].strip(),
                    }
                except (ValueError, KeyError):
                    # si una fila viene mal, la salto y sigo con las demás
                    errores.append("Fila " + str(numero_fila) + ": datos inválidos")
                    continue
                if agregar_producto(producto):
                    cargados = cargados + 1
                else:
                    errores.append("Fila " + str(numero_fila) + ": código repetido")
    except FileNotFoundError:
        errores.append("No se encontró el archivo " + str(ruta))
    return cargados, errores
