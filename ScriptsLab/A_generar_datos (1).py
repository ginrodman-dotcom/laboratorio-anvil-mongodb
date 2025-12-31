import pymongo
from pymongo import MongoClient
import random


URI = "mongodb+srv://ginrodman_db_user:X5xxELI2pqUdM3Va@tiendas.9gabutg.mongodb.net/?retryWrites=true&w=majority&appName=Tiendas"

try:
    client = pymongo.MongoClient(URI)
    print("✅ ¡Conexión exitosa a MongoDB Atlas! :D")
except Exception as e:
    print(f":C Error de conexión: {e}")
    exit()

db = client["Tienda"]


col_productos = db["Productos"]
col_empleados = db["Empleados"]
col_clientes = db["Clientes"]
col_ventas = db["Ventas"]



# C - CREATE
def crear_documento(coleccion, datos):
    try:
        resultado = coleccion.insert_one(datos)
        print(f"   -> Creado ID: {resultado.inserted_id}")
    except Exception as e:
        print(f"   Error al crear: {e}")

# R - READ
def leer_documentos(coleccion):
    print(f"\n--- Leyendo colección: {coleccion.name} ---")
    try:
        docs = coleccion.find()
        for doc in docs:
            print(doc)
    except Exception as e:
        print(f"   Error al leer: {e}")

# U - UPDATE
def actualizar_documento(coleccion, filtro_campo, valor_filtro, nuevos_datos):
    try:
        filtro = {filtro_campo: valor_filtro}
        accion = {"$set": nuevos_datos}
        coleccion.update_one(filtro, accion)
        print(f"   -> Actualizado donde {filtro_campo} = {valor_filtro}")
    except Exception as e:
        print(f"   Error al actualizar: {e}")

# D - DELETE
def eliminar_documento(coleccion, filtro_campo, valor_filtro):
    try:
        filtro = {filtro_campo: valor_filtro}
        coleccion.delete_one(filtro)
        print(f"   -> Eliminado donde {filtro_campo} = {valor_filtro}")
    except Exception as e:
        print(f"   Error al eliminar: {e}")








# ---  GENERACIÓN DE DATOS  ---

if __name__ == "__main__":
    print("\n---  INICIANDO CARGA DE DATOS ---")
    

    lista_generos = ["Rock", "Pop", "Jazz", "Salsa", "Electrónica", "Reggaeton", "Clásica", "Indie", "Rap"]
    lista_cargos = ["Vendedor", "Cajero", "Gerente", "Almacenero", "Seguridad", "Limpieza"]
    lista_pagos = ["Tarjeta Crédito", "Tarjeta Débito", "Efectivo", "Yape", "Plin"]

    lista_formatos = ["Vinilo", "CD", "Cassette"]



    # ---------------------------------------------------------
    # A. INSERTAR PRODUCTOS 
    # ---------------------------------------------------------
    print("\n Insertando Productos...")
    for i in range(1, 11):
        genero_random = random.choice(lista_generos)
        formato_random = random.choice(lista_formatos)

        producto = {
            "nombre": f"{formato_random} Vol. {random.randint(100, 999)}", 
            "artista_id": f"Artista 0{random.randint(1, 50)}",
            "genero": genero_random,
            "precio": random.randint(40, 150),      
            "stock": random.randint(5, 50),          
            "formato": formato_random
        }
        crear_documento(col_productos, producto)


    # ---------------------------------------------------------
    # B. INSERTAR EMPLEADOS 
    # ---------------------------------------------------------
    print("\n Insertando Empleados...")
    for i in range(1, 11):
        cargo_random = random.choice(lista_cargos)
        

        if cargo_random == "Gerente":
            sueldo = random.randint(3500, 5000)
        elif cargo_random == "Seguridad":
            sueldo = random.randint(1500, 1800)
        else:
            sueldo = random.randint(1200, 2000) 

        empleado = {
            "identificador": f"EMP-{random.randint(1000, 9999)}", 
            "cargo": cargo_random,
            "sueldo": sueldo,
            "turno": random.choice(["Mañana", "Tarde", "Noche"])
        }
        crear_documento(col_empleados, empleado)

    # ---------------------------------------------------------
    # C. INSERTAR CLIENTES
    # ---------------------------------------------------------
    print("\n Insertando Clientes...")
    for i in range(1, 11):
        edad_random = random.randint(18, 65)
        num_cliente = random.randint(100, 999)
        
        cliente = {
            "identificador": f"CLI-{num_cliente}",         
            "email": f"usuario{num_cliente}@gmail.com",    
            "edad": edad_random,
            "vip": random.choice(["SÍ", "NO"])      
        }
        crear_documento(col_clientes, cliente)

    # ---------------------------------------------------------
    # D. INSERTAR VENTAS
    # ---------------------------------------------------------
    print("\n Insertando Ventas...")
    for i in range(1, 11):
        pago_random = random.choice(lista_pagos)
        
        venta = {
            "folio": f"V-{2024}-{random.randint(1000, 9999)}",
            "total": random.randint(50, 500),   
            "metodo_pago": pago_random,
            "items_comprados": random.randint(1, 5)
        }
        crear_documento(col_ventas, venta)
    
    print("\n ¡LISTO! Nuevos datos agregados correctamente :3 ¡Muchas Gracias!")